"""Independent checks of unsuspended UI handoff observations, including failures."""
import copy,gzip,json,struct
from tools import school_native_dialogue_verification as source
ROOT=source.ROOT;need=source.need;word=source.word


def verify(report,action=None,require_transition=False):
 p=report['case']['probe'];h=p['input_handoff'];need(report['case']['system_input_expected'] is True,'separate UI phase expected')
 # Reuse the frozen-scene/no-input checks for their stated phase only. This
 # projection is NOT evidence that the whole run had no system input.
 baseline=copy.deepcopy(report);baseline['case']['system_input_expected']=False;baseline['input_method']='no input observation'
 for k in ('press_index','release_index','advanced_index'):baseline['case']['probe']['dialogue_boundary'][k]=None
 core=source.verify_report(baseline);window=report['case']['lifecycle']['ready']['window'];game=report['case']['lifecycle']['ready']['game']['pointer'];pc=p['dialogue_boundary']['wait_PC'];contents=bytes.fromhex(p['script_file']['loaded_memory_hex'])
 need(h['thread_suspension_used'] is False and h['existing_process_memory_written'] is False,'unsuspended read-only handoff')
 for phase in ('window_before','window_after'):
  d=h[phase];need((d['hwnd'],d['pid'],d['tid'])==(window['hwnd'],window['pid'],window['tid']) and d['visible'] is True and d['enabled'] is True and d['iconic'] is False and d['hung'] is False and d['window_state_written'] is False,'actual usable owned handoff window')
  need(d['cloaked_status']==0 and d['cloaked']==0 and d['window_desktop']==d['observer_desktop']=='Default','uncloaked same-desktop observation')
 rows=h['samples'];need(1<=len(rows)<=30000 and [s['index'] for s in rows]==list(range(len(rows))),'complete bounded handoff sequence');need(h['wait_PC']==pc,'same original confirmation wait')
 last=p['samples'][p['dialogue_boundary']['ready_index']]['wall_time_ns'];press=release=advance=None;keyboard=[];mouse=[];os_events=[];query=source.OriginalKeyQuery()
 for s in rows:
  need(type(s['wall_time_ns'])is int and last<=s['wall_time_ns'] and h['started_wall_time_ns']<=s['wall_time_ns']<=h['ended_wall_time_ns'],'ordered actual handoff timestamps');last=s['wall_time_ns'];v=bytes.fromhex(s['VM_hex']);x=s['input'];body=bytes.fromhex(x['hex']);buttons=bytes.fromhex(x['mouse_hex'])
  need(x['game']==game and x['pointer']==game+0x10b8 and len(body)==0xa00 and len(buttons)==8 and len(v)==128,'complete read-only actual game/VM/keyboard/mouse extents')
  need(word(v,16)==p['script_file']['loaded_pointer']+452 and word(v,28)<=len(contents)-452,'original loaded script address/PC range')
  key=query.query(body);need(key==int(bool(body[0x4b9]&128)),'raw original query against asynchronously observed bytes')
  button=word(buttons,4)&7
  if key:keyboard.append(s['index'])
  if button:mouse.append(s['index'])
  if s.get('os_space_state') not in (None,0):
   need(s['foreground_hwnd']==window['hwnd'] and type(s['os_space_state'])is int and 0<=s['os_space_state']<=65535,'OS key diagnostic only in owned foreground');os_events.append(dict(index=s['index'],state=s['os_space_state']))
  if (key or button) and press is None:press=s['index']
  if press is not None:
   if not key and not button and release is None:release=s['index']
   if word(v,28)!=pc and advance is None:advance=s['index']
 need((h['press_index'],h['release_index'],h['advanced_index'])==(press,release,advance),'cached handoff boundary derived from actual source input/VM bytes')
 verified=False
 if require_transition:
  action=action or h.get('action_receipt');need(action is not None,'successful authorized input receipt required')
  need(not mouse and word(bytes.fromhex(rows[0]['VM_hex']),28)==pc and not bytes.fromhex(rows[0]['input']['hex'])[0x4b9]&128,'initial unchanged confirmation and keyboard-only transition')
  need(press is not None and release is not None and advance is not None and press<release and press<=advance,'real input/release/PC transition required')
  need(s['foreground_hwnd']==window['hwnd'],'owned foreground at handoff end')
  need(h.get('backend')=='held scan-code fallback' and report['input_method']=='guarded Win32 held scan code; no host object writes','explicit held input backend identity')
  need(action['method']=='guarded Win32 SendInput held scan code' and action['input_returned'] is True and action['released'] is True and action['down_submitted'] is True and action['up_attempted'] is True and action['down_result']==1 and action['up_results']==[1],'real held-key down/up receipt')
  need(action['scan_code']==0x39 and action['hold_ms']==120 and action['existing_process_memory_written'] is False,'bounded source-space scan code only')
  need((action['hwnd'],action['pid'])==(window['hwnd'],window['pid']) and __import__('pathlib').Path(action['process_image']).resolve()==__import__('pathlib').Path(p['process_image']).resolve(),'receipt actual private HWND/PID/image')
  need(action['up_ns']-action['down_ns']>=120000000 and action['start_ns']<=action['down_ns']<action['up_ns']<=action['end_ns'],'actual bounded hold duration')
  need(h['started_wall_time_ns']<=action['start_wall_time_ns']<=action['down_wall_time_ns']<action['up_wall_time_ns']<=action['end_wall_time_ns']<=h['ended_wall_time_ns'],'input receipt inside actual observation interval')
  need(action['down_wall_time_ns']-10000000<=rows[press]['wall_time_ns']<=action['up_wall_time_ns']+100000000 and rows[release]['wall_time_ns']>=action['up_wall_time_ns']-10000000,'actual observed press/release temporally matches held input')
  need(keyboard and all(x['foreground_hwnd']==window['hwnd'] for x in rows[press:release+1]),'original keyboard captured under owned foreground')
  activation=p['owned_window_activation'];need(activation['hwnd']==activation['after']==window['hwnd'] and all(x['name']=='SetForegroundWindow' for x in activation['operations']),'only the actual owned window was activated')
  need(word(bytes.fromhex(p['samples'][-1]['VM_hex']),28)!=pc,'post-input original ordinary loop crossed confirmation PC')
  verified=True
 return dict(schema_version=1,core_scene_and_no_input_phase=core,samples=len(rows),keyboard_pressed_samples=keyboard,mouse_confirmation_samples=mouse,OS_space_events=os_events,derived_boundary=dict(press_index=press,release_index=release,advanced_index=advance),read_mode='unsuspended separate memory reads; not an atomic full-state or instruction trace',system_input_transition_verified=verified,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);p.add_argument('--require-transition',action='store_true');a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable handoff proof path required')
 r=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())),require_transition=a.require_transition);out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('read-only handoff verified; OS observations',len(r['OS_space_events']),'game input/PC',r['derived_boundary'])
