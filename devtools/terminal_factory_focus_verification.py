"""Independent factory-focus receipt binding above frozen retention checks.

The optional factory-only mode validates startup observations, never a complete
school continuation, full API trace, resource cleanup, or formal acceptance.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PureWindowsPath

from devtools import terminal_worker_retention_verification_v2 as retention

frozen=retention.frozen
need=frozen.need
ROOT=retention.ROOT
identity=retention.identity
RETENTION_SHA='8291a9534fc87e5afb8c2b162d98b64ee20f64ee78406788430130a5cd70134c'
LAYER_IDENTITIES=(
    ('devtools/terminal_menu_handoff.py','154efedd03310eee9321c71dd975903ae432dca7f48b5db8ad51f82bc97e9079'),
    ('tools/school_startup_lifetime.py','9199bbd3a645b9a3886ca8309cd46be466582812beb396b1446d85c826deef9b'),
    ('devtools/terminal_factory_focus.py','84328f32f5f7cf3651e1e4ea6a3acffdcf2f1183e6ea7412e435966e9adf5981'))
ENCODING='UTF-8 JSON sort_keys=True,separators=(comma,colon),ensure_ascii=False'


def canonical(value):
    data=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())


def verify_observation(report):
    receipt=report['factory_focus_observation'];life=report['lifecycle']
    need(receipt['schema_version']==1 and receipt['kind']=='factory_and_ready_before_automatic_focus',
         'explicit factory and ready focus gate receipt')
    need(receipt['capture_hook_restored']is True and receipt['scope_errors']==[],
         'capture hook restored with no scope identity or restoration failure')
    need(all(receipt[k]is False for k in ('accepted','activation_success_inferred','full_factory_trace_proved'))
         and all(receipt[k]==[]for k in ('host_game_calls','host_memory_writes','host_input_actions')),
         'focus adapter makes no injected input or full-proof claim')
    rows=receipt['implementations']
    need(len(rows)==3 and rows==receipt['implementations_after'],'exact unchanged three-layer focus implementation')
    for declared,(relative,digest)in zip(rows,LAYER_IDENTITIES):
        actual=identity(ROOT/relative);path=PureWindowsPath(declared['path']);parts=Path(relative).parts
        need(actual['sha256']==digest and path.name==parts[-1] and path.parent.name==parts[-2] and
             all(declared[k]==actual[k]for k in ('bytes','sha256')),'fixed executed focus adapter and original observers')
    need(receipt['qualification']==report['input_isolation'],'same source guest qualification before scope')
    isolation=frozen.verify_input_isolation(report['input_isolation'])
    need(life['factory']is not None and life['ready']is not None,'actual factory and initialized-loop captures')
    factory=life['factory'];ready=life['ready'];pid=ready['pid'];window=ready['window'];g=ready['globals']
    need(factory['pid']==pid==window['pid'],'same factory ready and HWND owner')
    raw=frozen.menu.contract.read_source()
    # The original source file is already pinned above; parse only its literal
    # read-range declaration rather than importing a native collector.
    tree=ast.parse((ROOT/LAYER_IDENTITIES[1][0]).read_text(encoding='utf8'))
    ranges=[ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)
            and any(isinstance(t,ast.Name)and t.id=='RANGES'for t in n.targets)]
    need(len(ranges)==1,'one original lifecycle code-range declaration')
    expected=[dict(va=a,bytes=b-a,sha256=hashlib.sha256(raw[a-0x400000:b-0x400000]).hexdigest())for a,b in ranges[0]]
    for snapshot in (factory,ready):
        need(snapshot['source']==expected,'complete original live factory/WinMain code identity receipts')
        for frame in snapshot['frames']:frozen.owner.verify_frame(frame)
    factory_tids=[f['tid']for f in factory['frames']if
        {0x49DF8A,0x45060F}<={x['return_va']for x in f['chain']}]
    need(factory_tids and any({0x49DF8A,0x45060F,0x5714E6}<={x['return_va']for x in f['chain']}
         for f in factory['frames']),'same original factory and WinMain/CRT ancestry')
    need(any(0x49DFD1<=f['EIP']<0x49E092 or any(0x49DFD1<=x['return_va']<0x49E092
         for x in f['chain'])for f in ready['frames']),'actual ready WinMain-loop frame')
    need(factory['globals']['0x7a49fc']==factory['globals']['0x80a398']==0 and
         factory['globals']['0x7a4a00']==g['0x7a4a00'] and
         factory['globals']['0x7a0bb4']==g['0x7a0bb4']==window['hwnd'],
         'fresh factory globals and same original main window')
    for name,key,size in (('main','0x7a4a00',0x1110),('game','0x7a49fc',0xBA20),('cache','0x80a398',176)):
        need(ready[name]['pointer']==g[key] and g[key]>0,'actual published ready '+name)
        frozen.blob(ready[name]['hex'],size,'complete original ready '+name)
    captures=receipt['captures'];need(len(captures)==2,'exact factory and ready capture bindings')
    for i,(kind,snapshot)in enumerate((('factory',factory),('ready',ready))):
        row=captures[i];digest=canonical(snapshot)
        need(row['kind']==kind and row['pid']==pid and row['elapsed']==snapshot['elapsed'] and
             row['capture_returned']is True and row['canonical_encoding']==ENCODING and
             (row['original_capture_bytes'],row['original_capture_sha256'])==(digest['bytes'],digest['sha256']) and
             row['factory_frame_tids']==(factory_tids if i==0 else []),'exact canonical original '+kind+' capture')
    resumes=receipt['focused_members_resumed'];need(len(resumes)==1,'one same-owner original focus dispatch gate')
    resumed=resumes[0]
    need(resumed['pid']==pid and (resumed['factory_capture_index'],resumed['ready_capture_index'])==(0,1) and
         resumed['original_focused_members_dispatched']is True and resumed['activation_success_claimed']is False,
         'gate references exact captured objects without invented focus success')
    need(type(receipt['deferred_members_calls'])is int and receipt['deferred_members_calls']>=1,
         'original membership enumeration actually deferred automatic focus')
    activations=report['startup_activation'];need(len(activations)==1,'actual original startup activation receipt')
    activation=activations[0]
    times=[frozen.number(x,'factory/focus elapsed')for x in (
        factory['elapsed'],ready['elapsed'],resumed['elapsed'],activation['elapsed'])]
    need(times[0]<times[1]<=times[2]<=times[3],'factory then ready precede original activation')
    if 'error'in activation:
        need(set(activation)=={'elapsed','error'} and isinstance(activation['error'],str),'unchanged actual activation failure')
        focus=dict(outcome='original_activation_failed',error=activation['error'])
    else:
        observed=frozen.verify_guest_focus(activation,isolation,pid,window['hwnd'])
        focus=dict(outcome='original_activation_verified',path=observed['path'])
    return dict(status='partial_factory_focus_observation',accepted=False,pid=pid,
        factory_elapsed=times[0],ready_elapsed=times[1],focused_members_elapsed=times[2],activation_elapsed=times[3],
        canonical_factory=canonical(factory),canonical_ready=canonical(ready),activation=focus,
        deferred_members_calls=receipt['deferred_members_calls'],capture_hook_restored=True,
        implementations=rows,qualification={k:receipt['qualification'][k]for k in
            ('path','bytes','sha256','current_guest_uuid','current_guest_boot_utc','current_guest_resources')},
        full_factory_trace_proved=False,full_school_source_verified=False,
        full_resource_lifetime_proved=False,PTDcleanup=False)


def verify_file(path,digest,guest_modules=None,factory_only=False):
    need(identity(retention.__file__)['sha256']==RETENTION_SHA,'fixed independent retention verifier')
    report=frozen.read_report(path,digest);focus=verify_observation(report)
    if factory_only:
        return dict(status='partial_factory_focus_observation',accepted=False,factory_focus=focus,
                    full_school_source_verified=False,source=identity(path))
    result=retention.verify_file(path,digest,guest_modules)
    result['factory_focus']=focus
    return result


def execution_identities():
    return [identity(p)for p in (__file__,retention.__file__,retention.v1.__file__,frozen.__file__)]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True);parser.add_argument('--source-sha',required=True)
    parser.add_argument('--guest-modules');parser.add_argument('--factory-only',action='store_true')
    parser.add_argument('--out',required=True)
    a=parser.parse_args();out=Path(a.out);need(not out.exists(),'fresh independent proof path')
    before=execution_identities()
    try:result=verify_file(a.source,a.source_sha,a.guest_modules,a.factory_only)
    except Exception as exc:result=dict(status='blocked',error=repr(exc),accepted=False)
    result.update(execution_implementations=before,execution_implementation_errors=[])
    try:
        after=execution_identities();result['execution_implementations_after']=after
        if before!=after:result['execution_implementation_errors'].append('verification implementation changed')
    except Exception as exc:result['execution_implementation_errors'].append(repr(exc))
    if result['execution_implementation_errors']:
        result.update(status='blocked',accepted=False,worker_retention_verified=False)
    data=json.dumps(result,ensure_ascii=False,indent=2).encode();need(len(data)<=512*1024,'bounded independent summary')
    with out.open('xb')as stream:stream.write(data+b'\n')
    return 2 if result['status']=='blocked' else 0


if __name__=='__main__':raise SystemExit(main())
