"""Verify the saved REA session against immutable PE bytes; no process launch."""
import hashlib
import json
from pathlib import Path
import re

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

from tools.rea_native_pilot import evidence

ROOT = Path(__file__).resolve().parents[1]
SESSION = ROOT / '.venv-audit/rea-wait-20261113/run-v1'
OUT = ROOT / 'analysis/terminal-rea-wait-chain-review-v1-20261113.json'


def need(value, message):
    if not value:
        raise ValueError(message)


def identity(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    need(not OUT.exists(), 'fresh review output required')
    run = json.loads((SESSION/'run.json').read_bytes())
    need(run['completed'] and run['closed'] and run['server_exit_code'] == 0, 'complete closed REA session')
    need(len(run['queries']) == 31 and not any(q['is_error'] for q in run['queries']), 'all real queries')
    image = ROOT/'analysis/hermit_game.exe'
    need(identity(image)['sha256'] == run['target_before']['sha256'] ==
         run['target_after']['sha256'] == '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005',
         'immutable original source')
    for row in run['implementations']:
        p = Path(row['path'])
        need(hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256'], 'executed implementation unchanged')
    pe = pefile.PE(str(image)); md = Cs(CS_ARCH_X86, CS_MODE_32)
    def raw_at(va, size):
        return pe.get_data(va-pe.OPTIONAL_HEADER.ImageBase, size)
    def get(label):
        envelope = json.loads((SESSION/(label+'.json')).read_bytes())
        need(not envelope.get('isError'), label)
        d = evidence(envelope)
        need(d['subject']['digest']['sha256'] == run['target_before']['sha256'], 'query subject')
        return d
    bytes_rows = []
    for q in run['queries']:
        if q['tool'] != 'read_bytes':
            continue
        row = get(q['label'])['normalized_result']
        va = int(row['address'], 16); data = bytes.fromhex(row['bytes_hex'])
        need(row['complete'] and len(data) == row['requested_bytes'] == row['returned_bytes'], 'complete byte query')
        need(raw_at(va,len(data)) == data, 'REA bytes match raw PE, not decompiler constants')
        bytes_rows.append({'va': va, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    functions = []; listings = {}
    aliases = {'JNZ':'jne', 'JZ':'je', 'STOSD.REP':'rep stosd', 'SAL':'shl',
               'JNC':'jae', 'JC':'jb', 'JNA':'jbe', 'JNBE':'ja'}
    for q in run['queries']:
        if q['tool'] != 'procedure_assembly':
            continue
        d = get(q['label']); lines = d['normalized_result'].splitlines()
        addresses = []
        for line in lines:
            m = re.fullmatch(r'(0x[0-9a-f]+): (\S+)(?: (.*))?', line)
            need(m is not None, 'listing syntax')
            va = int(m[1],16); decoded = next(md.disasm(raw_at(va,15),va))
            expected = aliases.get(m[2],m[2].lower())
            need(decoded.mnemonic == expected, 'independent mnemonic '+hex(va)+' '+decoded.mnemonic+' '+expected)
            addresses.append(va); listings[va] = line
        need(addresses == sorted(set(addresses)), 'ordered distinct listing sites')
        functions.append({'entry': q['arguments']['procedure'], 'instruction_sites': len(addresses),
                          'last_instruction': lines[-1], 'function_limitations': d['raw_result'].get('limitations',[])})
    expected = {
        0x422407: ('call','dword ptr [0x59226c]'),
        0x42240D: ('cmp','esi, esp'),
        0x42241C: ('call','0x4225a0'),
        0x422431: ('ret','4'),
        0x4225CE: ('mov','dword ptr [eax + 4], edx'),
        0x4539FB: ('call','0x453f10'),
        0x453A00: ('mov','dword ptr [ebp - 8], eax'),
        0x453CB0: ('call','0x422360'),
        0x453CB5: ('cmp','dword ptr [ebp - 8], 0'),
        0x453CB9: ('je','0x453ce4'),
        0x453CC4: ('call','0x4967b0'),
        0x453CCE: ('call','0x422360'),
        0x453CD8: ('call','0x422360'),
        0x453CDD: ('mov','eax, 1'),
        0x453CE4: ('jmp','0x4539cd'),
        0x453CFB: ('ret',''),
        0x4967D0: ('call','0x496410'),
        0x4967DB: ('jmp','0x496898'),
        0x496430: ('movsx','ecx, byte ptr [eax + 0x117c3c]'),
        0x496437: ('cmp','ecx, 1'),
        0x496810: ('call','0x56e7c0'),
        0x4968A8: ('ret',''),
    }
    checks = []
    for va, wanted in expected.items():
        i = next(md.disasm(raw_at(va,15),va))
        need((i.mnemonic,i.op_str) == wanted and va in listings, 'actual key chain '+hex(va))
        checks.append({'va': hex(va), 'hex': i.bytes.hex(), 'independent': i.mnemonic+' '+i.op_str,
                       'REA_listing': listings[va]})
    caller_empty = get('4539b0-procedure_callers')['normalized_result']
    external = next(md.disasm(raw_at(0x451AB7,5),0x451AB7))
    need(caller_empty == [] and (external.mnemonic,external.op_str)==('call','0x4539b0'), 'explicit incomplete caller counterexample')
    report = {'kind':'rea-wait-chain-source-review', 'review_passed':True, 'accepted':False,
              'original_game_observed':False, 'formal_progress':'2/8',
              'session':identity(SESSION/'run.json'), 'source':identity(image),
              'reviewer':identity(Path(__file__)), 'tool_calls':31,
              'session_seconds':run['elapsed_seconds'], 'raw_byte_queries':bytes_rows,
              'independently_decoded_listing_sites':sum(x['instruction_sites'] for x in functions),
              'functions':functions, 'key_instructions':checks,
              'interpretation':[
                  '4539FB obtains the scene result and 453A00 stores it in the caller frame. 453CB5 tests this retained result after 422360 returns; it does not test a wait API EAX result.',
                  '422407 calls the original wait import. On a balanced-stack normal path, the tail checks ESP, clears flag 0x10000 through 4225A0 and RET 4 at 422431. No new compulsory OS/file boundary appears before 453CB5.',
                  'Nonzero scene result calls 4967B0 with this+0x190, then two more original waits at 453CCE and 453CD8, and only then MOV EAX,1 and the original return. Zero scene result loops to 4539CD.',
                  '4967B0 only opens ReplayData.rep when byte[this+117C3C] equals 1. Its file event is optional and after the first result read. This cannot substitute for that earlier boundary.',
                  'Actual wait success and real peer signaling remain external proof obligations because 422360 does not branch on wait status. No live handshake is inferred from static flow.'
              ],
              'REA_limitations':[
                  'Seven entries and 214 IAT names were supplied as prior analyst hints; these are not independent discoveries.',
                  'Callers(4539B0) is empty despite raw 451AB7 calling it. Unseeded/indirect callers are not exhaustively discovered; empty xrefs at an interior return site do not disprove the return edge.',
                  'Decompiler still folds old imported API pointer values and loses thiscall/signatures. Stack-check helper is sometimes printed as the apparent source of an API result. Use original listing/bytes/ABI instead of copying pseudocode.',
                  'Per-function terminal-call warnings in assert/INT3 branches are preserved. Normal tail reasoning is conditional on original balanced ABI and excludes assertion failure paths.',
                  'All listing mnemonics were independently decoded; only the enumerated key operands were asserted. This is not complete semantic equivalence or dynamic execution.'
              ],
              'caller_coverage_counterexample':{'REA_callers':caller_empty,'original_call_va':'0x451ab7',
                  'hex':external.bytes.hex(),'target':'0x4539b0'},
              'files':[identity(x) for x in sorted(SESSION.iterdir()) if x.is_file()]}
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'review_passed':True,'calls':31,'listing_sites':report['independently_decoded_listing_sites'],
                      'key_operands':len(checks),'source_bytes':sum(x['bytes'] for x in bytes_rows)}))


if __name__ == '__main__':
    main()
