"""Fail-closed restoration tests on a small complete architectural fixture."""
import copy
from types import SimpleNamespace
import unittest

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ECX
from devtools import terminal_wait_probe as probe
from tools.terminal_unit_frontends_trace import MemoryDigest


class WaitProbeTests(unittest.TestCase):
    def setUp(self):
        self.task = 0x13000000
        uc = Uc(UC_ARCH_X86, UC_MODE_32)
        uc.mem_map(probe.WAIT & -4096, 4096, 5)
        uc.mem_map(probe.STACK, 0x20000, 3)
        uc.mem_map(self.task, 4096, 3)
        uc.reg_write(UC_X86_REG_EIP, probe.WAIT)
        uc.reg_write(UC_X86_REG_ECX, self.task)
        registers = probe.cpu(uc)
        digest = MemoryDigest(uc).capture()
        event = dict(pc=probe.WAIT, stop=True, continues_guest=False,
                     effects=[], CPU_changes={})
        tx = dict(driver=[], events=[event], after_CPU=registers,
                  after_memory=digest, after_trace={})
        self.row = dict(
            unit_frontends=dict(execution=dict(initial_regions=list(uc.mem_regions()),
                                               transactions=[tx])),
            forward_memory=[dict(pointer=a, bytes=b-a+1,
                                 hex=bytes(uc.mem_read(a, b-a+1)).hex())
                            for a, b, _ in uc.mem_regions()],
            forward_CPU=registers,
            frontier=dict(stack_hex=bytes(uc.mem_read(probe.STACK, 0x20000)).hex()))
        self.source = SimpleNamespace(previous=SimpleNamespace(TASK=self.task))

    def restore(self, row=None):
        return probe.restore(self.row if row is None else row, self.source)

    def test_complete_fixture_restores_exactly(self):
        uc, parent = self.restore()
        self.assertEqual(probe.cpu(uc), self.row['forward_CPU'])
        self.assertEqual(parent['memory'], MemoryDigest(uc).capture())

    def test_changed_memory_rejected(self):
        self.row['forward_memory'][-1]['hex'] = '01'+self.row['forward_memory'][-1]['hex'][2:]
        with self.assertRaisesRegex(ValueError, 'RAM and permissions'):
            self.restore()

    def test_changed_mapping_permission_rejected(self):
        regions = self.row['unit_frontends']['execution']['initial_regions']
        a, b, _ = regions[0]
        regions[0] = (a, b, 7)
        with self.assertRaisesRegex(ValueError, 'RAM and permissions'):
            self.restore()

    def test_missing_register_rejected(self):
        self.row['forward_CPU'] = copy.deepcopy(self.row['forward_CPU'])
        del self.row['forward_CPU']['XMM7']
        with self.assertRaisesRegex(ValueError, 'complete parent CPU'):
            self.restore()

    def test_wrong_entry_or_receiver_rejected(self):
        for register in ('EIP', 'ECX'):
            row = copy.deepcopy(self.row)
            row['forward_CPU'][register] = 0
            with self.subTest(register=register), self.assertRaisesRegex(ValueError, 'complete parent CPU'):
                self.restore(row)

    def test_cpu_mismatch_with_parent_transaction_rejected(self):
        self.row['forward_CPU'] = copy.deepcopy(self.row['forward_CPU'])
        self.row['forward_CPU']['EAX'] ^= 1
        with self.assertRaisesRegex(ValueError, 'complete parent CPU'):
            self.restore()

    def test_missing_memory_region_rejected(self):
        self.row['forward_memory'].pop()
        with self.assertRaisesRegex(ValueError, 'all authenticated forward memory regions'):
            self.restore()

    def test_changed_stack_claim_rejected(self):
        self.row['frontier']['stack_hex'] = '00'
        with self.assertRaisesRegex(ValueError, 'whole authenticated scene stack'):
            self.restore()

    def test_nonquiescent_parent_stop_rejected(self):
        for key, value in (('stop', False), ('continues_guest', True),
                           ('effects', [dict(kind='reg_write', register=1, value=1)]),
                           ('CPU_changes', dict(EAX=1))):
            row = copy.deepcopy(self.row)
            row['unit_frontends']['execution']['transactions'][0]['events'][0][key] = value
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, 'untouched parent wait stop'):
                self.restore(row)

    def test_absent_parent_wait_rejected(self):
        self.row['unit_frontends']['execution']['transactions'][0]['events'] = []
        with self.assertRaisesRegex(ValueError, 'missing authenticated parent wait'):
            self.restore()

    def test_topology_ledger_matches_actual_unicorn_after_map_protect_unmap(self):
        uc = Uc(UC_ARCH_X86, UC_MODE_32)
        uc.mem_map(0x1000, 0x3000, 7)
        actions = [dict(kind='mem_protect', address=0x2000, bytes=0x1000, permission=3),
                   dict(kind='mem_unmap', address=0x1000, bytes=0x1000),
                   dict(kind='mem_map', address=0x1000, bytes=0x1000, permission=1),
                   dict(kind='mem_map', address=0x5000, bytes=0x2000, permission=5)]
        for action in actions:
            args = [action['address'], action['bytes']]
            if 'permission' in action:
                args.append(action['permission'])
            getattr(uc, action['kind'])(*args)
        execution = dict(initial_regions=[(0x1000, 0x3FFF, 7)], transactions=[
            dict(driver=actions, events=[dict(pc=probe.WAIT, stop=True,
                                            continues_guest=False, effects=[], CPU_changes={})])])
        _, _, pages = probe.topology_at_wait(execution)
        actual = {page: permission for a, b, permission in uc.mem_regions()
                  for page in range(a, b+1, 4096)}
        self.assertEqual(pages, actual)

    def test_invalid_topology_rejected(self):
        for action in (
            dict(kind='mem_map', address=0x1000, bytes=0x1000, permission=3),
            dict(kind='mem_unmap', address=0x5000, bytes=0x1000),
            dict(kind='mem_protect', address=0x5000, bytes=0x1000, permission=3),
            dict(kind='mem_map', address=0x5001, bytes=0x1000, permission=3),
            dict(kind='mem_map', address=0x5000, bytes=0, permission=3),
            dict(kind='mem_map', address=0x5000, bytes=0x1000, permission=8),
            dict(kind='mem_map', address=0xFFFFF000, bytes=0x2000, permission=3),
        ):
            execution = dict(initial_regions=[(0x1000, 0x1FFF, 7)], transactions=[
                dict(driver=[action], events=[])])
            with self.subTest(action=action), self.assertRaises(ValueError):
                probe.topology_at_wait(execution)

    def test_compaction_preserves_partition_hash_all_bytes_and_permissions(self):
        original = Uc(UC_ARCH_X86, UC_MODE_32)
        for address in (0x1000, 0x2000, 0x3000):
            original.mem_map(address, 4096, 3)
            original.mem_write(address, bytes([address // 4096])*4096)
        partition = list(original.mem_regions())
        compact = Uc(UC_ARCH_X86, UC_MODE_32)
        for a, b, permission in probe.compact_regions(partition):
            compact.mem_map(a, b-a+1, permission)
            compact.mem_write(a, bytes(original.mem_read(a, b-a+1)))
        self.assertEqual(len(list(compact.mem_regions())), 1)
        self.assertEqual(len(partition), 3)
        self.assertEqual(MemoryDigest(original).capture(),
                         MemoryDigest(probe.PartitionView(compact, partition)).capture())

    def test_partition_view_rejects_wrong_actual_permissions(self):
        uc = Uc(UC_ARCH_X86, UC_MODE_32)
        uc.mem_map(0x1000, 0x3000, 3)
        uc.mem_protect(0x2000, 0x1000, 7)
        with self.assertRaisesRegex(ValueError, 'every page permission'):
            list(probe.PartitionView(uc, [(0x1000, 0x3FFF, 3)]).mem_regions())

    def test_partition_view_rejects_holes_or_extra_pages(self):
        for partition in ([(0x1000, 0x1FFF, 3), (0x3000, 0x3FFF, 3)],
                          [(0x1000, 0x4FFF, 3)]):
            uc = Uc(UC_ARCH_X86, UC_MODE_32)
            uc.mem_map(0x1000, 0x3000, 3)
            with self.subTest(partition=partition), self.assertRaisesRegex(ValueError, 'byte coverage'):
                list(probe.PartitionView(uc, partition).mem_regions())

    def test_compaction_does_not_merge_across_gaps_or_permissions(self):
        source = [(0x1000, 0x1FFF, 3), (0x2000, 0x2FFF, 3),
                  (0x3000, 0x3FFF, 5), (0x5000, 0x5FFF, 5)]
        self.assertEqual(probe.compact_regions(source),
                         [[0x1000, 0x2FFF, 3], [0x3000, 0x3FFF, 5], [0x5000, 0x5FFF, 5]])


if __name__ == '__main__':
    unittest.main()
