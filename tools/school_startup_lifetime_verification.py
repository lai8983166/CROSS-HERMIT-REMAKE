"""Cross-check original native observations, object graph and source branch probes."""
import argparse,hashlib,json,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_EAX,UC_X86_REG_EBP,UC_X86_REG_ESP,UC_X86_REG_EFLAGS
from tools.school_window_events import ROOT,SOURCE,SOURCE_SHA256,BASE

# Deliberately independent of the Windows observer's implementation.
BODIES=((0x49dd70,0x49e14a),(0x450350,0x45056c),(0x450570,0x45072b),
 (0x450730,0x4507c0),(0x413450,0x41355b),(0x413560,0x4136d0),
 (0x40d970,0x40d9ba),(0x4248e0,0x424978),(0x424980,0x424a89),
 (0x450d30,0x45104c),(0x49e150,0x49e1a0),(0x44fe60,0x44ffa0),
 (0x412dd0,0x412e30),(0x413190,0x413444),(0x416140,0x416255),
 (0x415f50,0x416133),(0x4010d0,0x40180d),(0x401810,0x401d20),
 (0x40dab0,0x40dc80),(0x5714d2,0x5714f2))
ORIGINAL_SHA='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7'

def need(value,why):
 if not value:raise ValueError(why)
def word(b,at=0):return struct.unpack_from('<I',b,at)[0]
def sha(b):return hashlib.sha256(b).hexdigest()
def chain_has(s,*addresses):
 return any(all(a in [r['return_va'] for r in f['chain']] for a in addresses) for f in s['frames'])
def native_loop(s):
 return any(0x49dfd1<=f['EIP']<0x49e092 or any(0x49dfd1<=r['return_va']<0x49e092 for r in f['chain']) for f in s['frames'])

def source_contract():
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA256,'source SHA')
 md=Cs(CS_ARCH_X86,CS_MODE_32);checks={
  0x4504dc:('mov','dword ptr [0x7a0bb4], eax'),
  0x4504fe:('call','dword ptr [0x592410]'),0x450513:('call','dword ptr [0x592414]'),
  0x45052d:('call','dword ptr [0x592424]'),0x450547:('call','dword ptr [0x592420]'),
  0x49def5:('call','dword ptr [0x592478]'),0x49df85:('call','0x450570'),
  0x45060a:('call','0x4135d0'),0x45063a:('call','0x413630'),
  0x45067a:('call','0x413450'),0x4506ac:('call','0x413560'),
  0x4506e9:('mov','dword ptr [eax], ecx'),0x4506eb:('xor','eax, eax'),
  0x4134de:('call','0x415f50'),0x413500:('call','0x40d970'),0x41350e:('call','0x40dab0'),
  0x40d993:('mov','dword ptr [eax], ecx'),0x40d9a2:('mov','dword ptr [ecx + 4], eax'),
  0x4010f9:('mov','dword ptr [eax + 0x58], ecx'),
  0x416005:('mov','dword ptr [edx + 0xb270], eax'),
  0x49de57:('jmp','0x49e092'),0x49df09:('jge','0x49df47'),
  0x49df35:('call','dword ptr [0x592398]'),0x49df96:('call','dword ptr [0x592398]'),
  0x450f6e:('call','dword ptr [0x592398]'),0x450f84:('call','dword ptr [0x59239c]'),
  0x424958:('call','dword ptr [0x5923e4]'),0x49e01a:('jmp','0x49e092'),
  0x49e0d9:('call','0x450730'),0x450792:('call','0x412dd0'),
  0x49e0f8:('call','0x49e150'),0x49e109:('mov','dword ptr [0x7a4a00], 0'),
  0x4133a8:('call','dword ptr [eax + 8]'),0x4133e5:('call','dword ptr [edx + 8]'),
  0x49e11f:('call','dword ptr [0x592474]'),0x49e147:('ret','0x10')}
 proof=[]
 for at,want in checks.items():
  i=next(md.disasm(raw[at-BASE:at-BASE+16],at));need((i.mnemonic,i.op_str)==want,'source contract '+hex(at))
  proof.append(dict(va=at,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 imports={}
 for at in range(0x5fd5cc,0x5fd6f8,20):
  desc=struct.unpack_from('<5I',raw,at-BASE)
  if not desc[0]:break
  dll=raw[desc[3]:].split(b'\0',1)[0].decode('ascii')
  index=0
  while word(raw,desc[0]+index*4):
   thunk=word(raw,desc[0]+index*4)
   name=('ordinal:'+str(thunk&65535)) if thunk&0x80000000 else raw[thunk+2:].split(b'\0',1)[0].decode('ascii')
   imports[hex(BASE+desc[4]+index*4)]=dict(dll=dll,symbol=name,descriptor=at);index+=1
 selected={hex(at):imports[hex(at)] for at in (0x592410,0x592414,0x592424,0x592420,0x592478,0x592474,0x59247c,0x592024,0x592398,0x59239c,0x5923e4,0x5923d8)}
 return dict(source_image_sha256=SOURCE_SHA256,bodies=[dict(va=a,bytes=b-a,sha256=sha(raw[a-BASE:b-BASE])) for a,b in BODIES],
  instructions=proof,imports=selected,execution_kind='native snapshots plus isolated source branch replay; not a complete instruction/API trace',
  factory_success_inference='4506E9 publishes only after renderer and post-renderer success; the observed same original caller reaches WinMain loop',
  warnings='4135D0 audio and413630 secondary setup failures warn and continue; publication alone does not prove their HRESULTs')

# Each probe is an explicitly declared isolated branch input, never an injected
# return in the native process or the retained VM. Stop before any external call.
PROBES=(('duplicate',0x49de53,'hwnd',None,0x49e092),
 ('window_failure',0x49decb,1,None,0x5923d8),
 ('COM_failure',0x49df05,0,(-0x38,0x80004005),0x5923d8),
 ('factory_failure',0x49df8a,1,None,0x592398),
 ('renderer_failure',0x45067f,1,None,0x5923d8),
 ('post_renderer_failure',0x4506b1,1,None,0x413360))

def branch_probes(hwnd):
 raw=SOURCE.read_bytes();reports=[];bp=0x31008000;sp=bp-0x200
 for name,start,eax,local,stop in PROBES:
  u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(BASE,(len(raw)+4095)&~4095);u.mem_write(BASE,raw)
  u.mem_map(0x31000000,65536);u.mem_write(0x31000000,b'\xa5'*65536)
  u.mem_write(0x7a0bb4,struct.pack('<I',hwnd));u.mem_write(bp+8,struct.pack('<I',hwnd))
  if local:u.mem_write(bp+local[0],struct.pack('<I',local[1]))
  target=word(raw,stop-BASE) if stop in (0x5923d8,0x592398) else stop
  if target>=BASE+len(raw) or target<BASE:u.mem_map(target&~4095,4096)
  init=dict(EIP=start,EBP=bp,ESP=sp,EAX=hwnd if eax=='hwnd' else eax,EFLAGS=0x202)
  for reg,key in ((UC_X86_REG_EIP,'EIP'),(UC_X86_REG_EBP,'EBP'),(UC_X86_REG_ESP,'ESP'),(UC_X86_REG_EAX,'EAX'),(UC_X86_REG_EFLAGS,'EFLAGS')):u.reg_write(reg,init[key])
  runs=[]
  def hook(uc,at,n,_):
   if at==target:uc.emu_stop();return
   need(BASE<=at<BASE+len(raw),'undeclared probe instruction')
   runs.append(dict(va=at,hex=bytes(uc.mem_read(at,n)).hex()))
  u.hook_add(UC_HOOK_CODE,hook);u.emu_start(start,0,count=200)
  need(u.reg_read(UC_X86_REG_EIP)==target,'branch probe boundary')
  outsp=u.reg_read(UC_X86_REG_ESP)
  nargs=4 if stop==0x5923d8 else 1 if stop==0x592398 else 0
  reports.append(dict(name=name,declared_cpu=init,declared_local=list(local) if local else None,hwnd=hwnd,instructions=runs,stop=target,
   final_esp=outsp,args=[word(bytes(u.mem_read(outsp+4+i*4,4))) for i in range(nargs)],
   external_call_executed=False,game_function_substituted=False,retained_VM_advanced=False))
 return reports

def verify_snapshot(s,contract):
 need(s['source']==contract['bodies'],'live original function identity')
 for f in s['frames']:
  b=bytes.fromhex(f['context_hex']);need(len(b)==716,'full WOW64 context')
  need((f['EIP'],f['EBP'],f['ESP'])==tuple(word(b,a) for a in (184,180,196)),'actual context scalars')
  if f['chain']:need(f['chain'][0]['bp']==f['EBP'],'actual frame root')
  for a,b in zip(f['chain'],f['chain'][1:]):need(a['saved_bp']==b['bp'] and a['bp']<b['bp']<a['bp']+0x100000,'bounded original frame chain')
 if 'winmain_frame' in s:
  f=s['winmain_frame'];b=bytes.fromhex(f['stack_hex']);bp=f['bp']
  need(f['stack_start']==bp-0xac and len(b)==0xd0,'complete sampled WinMain stack slice')
  need(b[0x10:0xac].hex()==f['locals_hex'] and b[0xb4:0xc4].hex()==f['args_hex'],'WinMain local/argument overlap')
  need(word(b,0xb0)==0x5714e6 and any(any(r['bp']==bp and r['return_va']==0x5714e6 for r in x['chain']) for x in s['frames']),'WinMain actual CRT caller')

def verify_lifetime(l):
 need(not l['forced_termination'] and not l['members_before_cleanup'] and not l['members_after_cleanup'],'no forced termination can stand for source cleanup')
 need(l['parent_pid'] and len(l['exits'])>=2 and all(x['signaled'] for x in l['exits'].values()),'owned original process tree exit')
 need(l['exits'][str(l['parent_pid'])]['code']==0,'protector parent outcome')
 need(all(x['code'] in (0,0xc0000354) for x in l['exits'].values()),'unexpected original exit status')
 need(l['membership'][-1]['pids']==[] and {int(p) for p in l['exits']}=={p for x in l['membership'] for p in x['pids']},'complete owned Job membership')
 need(l['child_status_is_not_WinMain_return'] is True,'do not confuse protection status with source return')

def epilogue(s):
 f=s['winmain_frame'];bp=f['bp'];b=bytes.fromhex(f['stack_hex']);raw=SOURCE.read_bytes()
 need(word(b,0xa8)==0,'sampled WinMain return local must be zero')
 u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(BASE,(len(raw)+4095)&~4095);u.mem_write(BASE,raw)
 page=(bp-0xac)&~4095;u.mem_map(page,8192);u.mem_write(bp-0xac,b)
 u.reg_write(UC_X86_REG_EBP,bp);u.reg_write(UC_X86_REG_ESP,bp-0xa8);u.reg_write(UC_X86_REG_EFLAGS,0x202)
 runs=[]
 def hook(uc,at,n,_):
  if at==0x5714e6:uc.emu_stop();return
  need(0x49e131<=at<0x49e14a or 0x56ce80<=at<0x56ce83,'epilogue undeclared source')
  runs.append(dict(va=at,hex=bytes(uc.mem_read(at,n)).hex()))
 u.hook_add(UC_HOOK_CODE,hook);u.emu_start(0x49e131,0,count=100)
 need(u.reg_read(UC_X86_REG_EIP)==0x5714e6 and u.reg_read(UC_X86_REG_EAX)==0 and u.reg_read(UC_X86_REG_ESP)==bp+24,'original ret10 source ABI/zero return')
 return dict(instructions=runs,EIP=u.reg_read(UC_X86_REG_EIP),EAX=u.reg_read(UC_X86_REG_EAX),ESP=u.reg_read(UC_X86_REG_ESP),
  declared_entry=0x49e131,sampled_stack_start=f['stack_start'],native_CRT_tail_executed_by_this_probe=False)

def verify_case(c,contract):
 need(c['error'] is None,'native original observation failed')
 for key in ('original_code_written','original_registers_written','original_IAT_written','retained_VM_advanced','resumable_checkpoint'):
  need(c[key] is False,'observation scope/integrity '+key)
 need(c['native_execution'] is True,'actual native execution required')
 initial=c['factory'];s=c['ready'];need(initial is not None and s is not None,'both original startup stages')
 for snap in [initial,s,*c['shutdown']]:verify_snapshot(snap,contract)
 need(chain_has(initial,0x45060f,0x49df8a,0x5714e6),'actual pre-publication factory ancestry')
 need(initial['globals']['0x7a49fc']==0 and initial['globals']['0x80a398']==0,'fresh native globals')
 need(initial['pid']==s['pid'] and initial['elapsed']<s['elapsed'] and native_loop(s),'same original startup reaches real WinMain loop')
 g=s['globals'];game=s['game']['pointer'];main=s['main']['pointer'];cache=s['cache']['pointer'];hwnd=g['0x7a0bb4']
 need(game and main and cache and (game,main,cache)==tuple(g[k] for k in ('0x7a49fc','0x7a4a00','0x80a398')),'actual object publications')
 need(initial['globals']['0x7a4a00']==main and initial['globals']['0x7a0bb4']==hwnd,'original main/window identity retained')
 mb=bytes.fromhex(s['main']['hex']);gb=bytes.fromhex(s['game']['hex']);cb=bytes.fromhex(s['cache']['hex'])
 need(len(mb)==0x1110 and len(gb)==0xba20 and len(cb)==176,'complete owner objects')
 need(word(mb)==0x5986a0 and word(mb,4)==hwnd,'original main vtable/window')
 w=s['window'];need(w['is_window'] and w['hwnd']==hwnd and w['pid']==s['pid'] and w['property']==main and w['find_window']==hwnd,'real window/property ownership')
 need(word(gb,0xb278)==1024 and word(gb,0xb27c)==768,'original startup dimensions')
 # Original game starts fullscreen (450671 pushes mode0), so B204 is not
 # required to carry HWND: this is distinct from older windowed experiments.
 device=word(gb,0xb210);factory=word(gb,0xb20c)
 need(device and factory and word(gb,0x1058)==game and word(gb,0x105c)==device,'original manager owner/device binding')
 need(word(gb,0x1060)==0x1000 and word(gb,0x1064)==0x100000,'source queue capacities')
 for q,off,n in zip(s['queues'],(0x1068,0x106c),(0x8000,0x100000)):
  need(q['offset']==off and q['pointer']==word(gb,off) and q['pointer'] and q['bytes']==n and len(q['sha256'])==64 and len(bytes.fromhex(q['head_hex']))==32 and len(bytes.fromhex(q['tail_hex']))==32,'actual accessible queue backing')
 need(len(s['queues'])==2,'both original queues')
 need(len(s['interfaces'])==5,'D3D and audio COM interfaces')
 for it,off in zip(s['interfaces'],(0xb20c,0xb210,0x1aa0,0x1aa4,0x1aa8)):
  ptr=word(gb,off)
  head=bytes.fromhex(it['head_hex']);table=bytes.fromhex(it['vtable_hex'])
  need(it['offset']==off and it['pointer']==ptr and len(head)==16 and word(head)==it['vtable'] and len(table)==64 and all(struct.unpack('<16I',table)),'actual native COM object/vtable')
  path=it['method_module'].lower().replace(chr(92),'/')
  need('/windows/syswow64/' in path and len(bytes.fromhex(it['first_method_hex']))==16,'actual x86 system COM implementation')
  if off in (0xb20c,0xb210):need(path.endswith('/d3d8.dll'),'actual D3D8 method module')
 need(word(cb,4)==device and word(cb,12) and word(cb,0x6c) and word(cb,0x98) and word(cb,0xa0),'real shared cache device/sprite/GDI bitmap backing')
 need(word(cb,0x70)==40 and word(cb,0x74)==256 and word(cb,0x78) in (256,0xffffff00),'original cache BITMAPINFO')
 sprite=s['cache_sprite'];sb=bytes.fromhex(sprite['hex'])
 need(sprite['pointer']==word(cb,12) and len(sb)==32 and word(sb)==0x5d1180 and word(sb,4)>0 and word(sb,8)==device,'actual cache sprite/device ownership')
 bitmap=s['cache_bitmap'];need(bitmap['pointer']==word(cb,0xa0) and bitmap['bytes']==256*256*4 and len(bitmap['sha256'])==64,'actual readable complete cache bitmap')
 need(len(s['fonts'])==3,'two bitmap fonts and static D3DX font')
 for font,off in zip(s['fonts'],(0x1090,0x1094,0xb270)):
  b=bytes.fromhex(font['hex']);need(font['offset']==off and font['pointer']==word(gb,off) and font['pointer'],'source font publication')
  if off!=0xb270:need(len(b)==0x678 and word(b,0x58)==device and word(b,0x5c) and word(b,0x60),'bitmap font device/texture/vertex resources')
  else:need(len(b)==80 and word(b)==0x5d1154 and word(b,4)>0 and word(b,8)>0 and word(gb,0xb26c)>0 and word(b,72)==cache and word(b,76)==device,'D3DX font and shared cache identity')
 wf=s['winmain_frame'];locals=bytes.fromhex(wf['locals_hex'])
 need(word(locals,0x9c-0x38)<0x80000000 and word(locals,0x9c-0x44)!=0,'actual COM and common-controls results')
 req=c['close_request'];need(req is not None and req['posted'] and req['hwnd']==hwnd and req['pid']==s['pid'] and req['pid'] in req['job_members'] and req['property']==main and (req['message'],req['wParam'],req['lParam'])==(16,0,0),'source-driven owned WM_CLOSE required')
 need(s['elapsed']<req['elapsed'],'close only after initialized observation')
 need(any(chain_has(x,0x49e0de,0x450797,0x412df5) for x in c['shutdown']),'actual original game destruction ancestry')
 finished=[x for x in c['shutdown'] if all(x['globals'][k]==0 for k in ('0x7a49fc','0x7a4a00','0x80a398')) and
  (any(0x49e11a<=r['return_va']<0x49e131 for f in x['frames'] for r in f['chain']) or chain_has(x,0x5714f2) and 'crt_exit' in x)]
 need(finished,'original game/main/cache teardown before CRT protection exit')
 need(c['window_after']==dict(is_window=False,property=0),'real window/property ended')
 verify_lifetime(c['lifetime'])
 dr=c['duplicate'];need(dr is not None and dr['error'] is None and dr['before_window']==hwnd==dr['after_window'],'real duplicate-run gate')
 need(all(not x['globals']['0x7a49fc'] and not x['globals']['0x7a0bb4'] for x in dr['observations']),'duplicate run must not publish another game/window')
 verify_lifetime(dr['lifetime']);need(set(dr['lifetime']['exits']).isdisjoint(c['lifetime']['exits']),'separate owned process trees')
 terminal=finished[-1];exit_result=None
 if 'crt_exit' in terminal:
  ce=terminal['crt_exit'];need(ce['WinMain_result_hex']==ce['exit_argument_hex']=='00000000','actual original CRT zero result')
  need(any(r['bp']==ce['callee_bp'] and r['saved_bp']==ce['caller_bp'] and r['return_va']==0x5714f2 for f in terminal['frames'] for r in f['chain']),'CRT caller frame identity')
  exit_result=ce
 return dict(pid=s['pid'],hwnd=hwnd,native_factory_to_loop=True,game=game,cache=cache,device=device,
  zeroed_original_globals=True,normal_game_cleanup_observed=True,protector_process_statuses=c['lifetime']['exits'],
  source_epilogue=epilogue(terminal) if 'winmain_frame' in terminal else None,actual_CRT_return=exit_result,
  failure_branch_probes=branch_probes(hwnd),retained_VM_advanced=False,
  complete_native_instruction_or_API_trace=False,live_resources_survive_capture=False)

def verify_report(report,check_producer=True):
 need(report['schema_version']==1 and report['source_image_sha256']==SOURCE_SHA256 and report['original_sha256']==ORIGINAL_SHA,'source report identity')
 if check_producer:need(report['observer_source_sha256']==sha((ROOT/'tools/school_startup_lifetime.py').read_bytes()),'frozen observer identity')
 need(len(report['cases'])==2,'two independent original runs')
 contract=source_contract();cases=[verify_case(c,contract) for c in report['cases']]
 need(cases[0]['pid']!=cases[1]['pid'],'independent original process observations')
 return dict(source_contract=contract,cases=cases,R1_original_initialization_and_game_cleanup=True,
  retained_VM_advanced=False,R2_render_connection_complete=False,
  native_game_cleanup_is_distinct_from_protector_CRT_tail=True,
  error_scope='Real duplicate-run exit; six isolated source branch probes stop before external calls, with declared inputs. No simulated API failure is reported as an actual OS result.')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh verification output required')
 r=verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))
 out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n')
 print('verified',len(r['cases']),'original factory/loop/teardown lifetimes; R2 retained VM unchanged',flush=True)
