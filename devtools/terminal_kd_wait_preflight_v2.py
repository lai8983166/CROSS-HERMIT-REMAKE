"""Bounded own-fixture kernel wait-tail probe, not user return qualification.

Uses a hardware execution breakpoint only inside the exact kernel's NtWait
tail. No user breakpoint, game process, memory write, or host input.
"""
import concurrent.futures as cf
import json
from pathlib import Path, PureWindowsPath
import re
import time
from devtools.isolated_windows_vm import WORKER, VMX, vmrun, identity
from devtools.isolated_vm_kd import run_guest, validate_kd_vmx
from devtools.isolated_vm_guest_admin import STATUS
from devtools.isolated_kd_engine_v7 import Engine


def need(value, message):
    if not value:
        raise ValueError(message)


def main():
    out = WORKER / 'kd-worker/wait-tail-v2.json'
    need(not out.exists(), 'fresh output')
    validate_kd_vmx(VMX.read_text(encoding='utf8'))
    folder = WORKER / 'vm-wait-fixture-v1-20261110'
    guest = PureWindowsPath('C:/ChaomofaWorker/kd-wait-tail-v2-20261110')
    q = str(guest)
    r = dict(accepted=False, fullstate=False, fullABI=False,
             original_game_started=False, host_input_actions=0, errors=[], stops=[])
    e = None
    ready = None
    launch = None
    pending = None
    pool = cf.ThreadPoolExecutor(max_workers=2)
    started = time.monotonic()

    def gates(names):
        return run_guest(';'.join("[IO.File]::WriteAllText('" + q + '\\' + name + "','continue')" for name in names) + ";'gates written'")

    def capture(command):
        return e.execute(command)

    try:
        r['guest_before'] = json.loads(run_guest(STATUS))
        run_guest("if(@(Get-Process 'CROSS HERMIT',python,pythonw,helper,fixture -ErrorAction SilentlyContinue).Count){throw 'busy'};if(Test-Path -LiteralPath '" + q + "'){throw 'fresh'};New-Item -ItemType Directory -Path '" + q + "'|Out-Null;'ready'")
        r['fixture_inputs'] = []
        for name in ('fixture.bin', 'manifest.json', 'terminal_vm_wait_fixture.cs', 'fixture.exe'):
            r['fixture_inputs'].append(identity(folder / name))
            vmrun(['CopyFileFromHostToGuest', VMX, folder / name, guest / name], guest=True)
        r['kernel'] = run_guest("(Get-FileHash -LiteralPath C:\\Windows\\System32\\ntoskrnl.exe -Algorithm SHA256).Hash").strip().lower()
        need(r['kernel'] == '5669b9b8bfcf20f08b7d1d65dc2deccbf836279c0e3f66722d72ad33ee7f672a', 'exact reviewed kernel')
        gates(['ack-0', 'ack-1', 'ack-2', 'ack-3'])
        command = "$p=Start-Process -FilePath '" + q + "\\fixture.exe' -ArgumentList @('--owned-vmm-fixture','" + q + "') -WindowStyle Hidden -PassThru;if(!$p.WaitForExit(180000)){throw 'bounded fixture lifespan'};[pscustomobject]@{exit_code=$p.ExitCode;result=if(Test-Path -LiteralPath '" + q + "\\result.json'){Get-Content -LiteralPath '" + q + "\\result.json' -Raw|ConvertFrom-Json}else{$null}}|ConvertTo-Json -Depth 10 -Compress"
        launch = pool.submit(run_guest, command)
        ready_command = "$end=[DateTime]::UtcNow.AddSeconds(10);while(!(Test-Path -LiteralPath '" + q + "\\ready.json')){if([DateTime]::UtcNow -gt $end){throw 'ready deadline'};Start-Sleep -Milliseconds 50};Get-Content -LiteralPath '" + q + "\\ready.json' -Raw"
        ready = json.loads(run_guest(ready_command))
        r['ready'] = ready
        need(ready['source_sha256'] == identity(folder / 'terminal_vm_wait_fixture.cs')['sha256'], 'fixture source')
        e = Engine()
        r['engine_identities'] = e.identities
        e.attach()
        e.interrupt()
        need(e.wait(15000), 'initial stop')
        r['target'] = capture('vertarget')
        r['module'] = capture('lm m nt')
        match = re.search(r'([0-9a-f]+`[0-9a-f]+)\s+[0-9a-f`]+\s+nt\s', r['module'])
        need(match, 'actual kernel base')
        base = int(match[1].replace('`', ''), 16)
        tail = base + 0x6fcc6a
        r['tail_before'] = capture('u %x L2' % tail)
        need('add     rsp,38h' in r['tail_before'] and 'ret' in r['tail_before'], 'reviewed tail bytes and decode')
        bp = 'ba e 1 %x ".if (@$tpid == 0x%x) { .if (@$tid == 0x%x) { .if (poi(@rbp-0x48) == 0x%x) { .echo OWNED_WAIT_RETURN } .else { gc } } .else { gc } } .else { gc }"' % (tail, ready['pid'], ready['tid'], ready['event_handle'])
        r['breakpoint_install'] = capture(bp)
        r['breakpoint_list'] = capture('bl')
        need(' e ' in r['breakpoint_list'], 'enabled kernel breakpoint')
        pending = pool.submit(gates, ['go'])
        for index, expected in enumerate((0, 0, 0, 258)):
            e.go()
            need(e.wait(15000), 'bounded owned kernel return')
            row = dict(index=index, registers=capture('r'), pid=capture('? @$tpid'),
                       tid=capture('? @$tid'), thread=capture('? @$thread'), process=capture('? @$proc'))
            r['stops'].append(row)
            regs = {k: int(v, 16) for k, v in re.findall(r'(\w+)=([0-9a-f]{16})', row['registers'])}
            need(regs.get('rip') == tail and regs.get('rax') == expected, 'actual kernel return PC and status')
            need(int(row['pid'].strip().split()[-1].replace('`', ''), 16) == ready['pid'], 'current process')
            need(int(row['tid'].strip().split()[-1].replace('`', ''), 16) == ready['tid'], 'current thread')
            row['stack'] = capture('dq %x L20' % regs['rsp'])
            row['trap'] = capture('dq %x L32' % (regs['rbp']-0x80))
            def qwords(text):
                words = {}
                for line in text.splitlines():
                    fields = line.split()
                    if fields and re.fullmatch('[0-9a-f]{8}`[0-9a-f]{8}', fields[0]):
                        address = int(fields[0].replace('`', ''), 16)
                        for j, value in enumerate(fields[1:]):
                            if re.fullmatch('[0-9a-f]{8}`[0-9a-f]{8}', value):
                                words[address+8*j] = int(value.replace('`', ''), 16)
                return words
            stack = qwords(row['stack'])
            trap = qwords(row['trap'])
            sp, bp0 = regs['rsp'], regs['rbp']
            row['arguments'] = dict(handle=trap.get(bp0-0x48), alertable=trap.get(bp0-0x40), user_rip=trap.get(bp0+0xe8), user_cs=trap.get(bp0+0xf0), caller=stack.get(sp+0x38), timeout_pointer=stack.get(sp+0x50), timeout_value=stack.get(sp+0x58))
            a = row['arguments']
            need(a['caller'] == base+0x428c35, 'original syscall dispatcher caller')
            need(a['handle'] == ready['event_handle'] and (a['alertable'] & 0xff) == 0, 'actual fixture response event and Alertable')
            need(a['user_cs'] & 0xffff == 0x33, 'WOW64 native syscall return mode')
            need(a['timeout_pointer'] == sp+0x58 and a['timeout_value'] == (0xfffffffffeced300 if index < 3 else 0), 'captured original relative timeout')
            row['fixture_count'] = capture('dq %x L1' % (ready['data']+0x200))
            need(qwords(row['fixture_count'])[ready['data']+0x200] & 0xffffffff == index, 'original fixture postcall sequence')
            row['user_syscall_tail'] = capture('u %x L8' % (a['user_rip']-2))
            need('0f05' in row['user_syscall_tail'].splitlines()[1], 'actual SYSCALL before saved RIP')
            row['kernel_context_only'] = True
        r['tail_after'] = capture('u %x L2' % tail)
        need(r['tail_before'] == r['tail_after'], 'no kernel byte patch')
        capture('bc *')
        r['breakpoints_after'] = capture('bl')
        need(not r['breakpoints_after'].strip(), 'owned breakpoint removed')
        e.go()
    except Exception as exc:
        r['errors'].append(repr(exc))
    finally:
        if e:
            try:
                if e.status() == 6:
                    e.execute('bc *')
                e.close()
                r['detached'] = True
            except Exception as exc:
                r['errors'].append('detach: ' + repr(exc))
            r['output'] = e.output
            r['calls'] = e.calls
        if ready:
            try:
                gates(['go', 'ack-0', 'ack-1', 'ack-2', 'ack-3'])
                script = "$end=[DateTime]::UtcNow.AddSeconds(10);while(!(Test-Path -LiteralPath '" + q + "\\result.json')){if([DateTime]::UtcNow -gt $end){throw 'result deadline'};Start-Sleep -Milliseconds 50};Get-Content -LiteralPath '" + q + "\\result.json' -Raw"
                r['fixture_result'] = json.loads(run_guest(script))
                result = r['fixture_result']
                need(result['error'] is None and result['returns'] == [0, 0, 0, 258] and not result['cleanup_errors'] and result['handles_closed'] and result['buffers_released'], 'normal fixture return and cleanup')
            except Exception as exc:
                r['errors'].append('fixture completion: ' + repr(exc))
        if launch:
            try:r['launch_result']=json.loads(launch.result(timeout=15))
            except Exception as exc:r['errors'].append('launcher: '+repr(exc))
        if pending:
            try:r['go_result']=pending.result(timeout=5)
            except Exception as exc:r['errors'].append('go: '+repr(exc))
        pool.shutdown(wait=True)
        try:
            r['guest_after'] = json.loads(run_guest(STATUS))
        except Exception as exc:
            r['errors'].append('guest: ' + repr(exc))
        r['elapsed_seconds'] = time.monotonic() - started
        with out.open('x', encoding='utf8') as f:
            json.dump(r, f, indent=2)
    print(json.dumps(dict(path=str(out), errors=r['errors'], kernel_stops=len(r['stops']), elapsed_seconds=r['elapsed_seconds'], accepted=False)))
    return bool(r['errors'])


if __name__ == '__main__':
    raise SystemExit(main())
