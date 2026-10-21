"""Adopt only a freshly tool-launched private original process tree into our Job."""
import ctypes as C,ctypes.wintypes as W,json,time
from pathlib import Path
from tools.school_native_scene import original,APP,image_name,sha,need


class PE(C.Structure):
 _fields_=[('size',W.DWORD),('usage',W.DWORD),('pid',W.DWORD),('heap',C.c_size_t),('module',W.DWORD),('threads',W.DWORD),('parent',W.DWORD),('priority',W.LONG),('flags',W.DWORD),('name',W.WCHAR*260)]


def private_processes():
 first=original.bind('Process32FirstW',W.BOOL,[W.HANDLE,C.POINTER(PE)]);nextp=original.bind('Process32NextW',W.BOOL,[W.HANDLE,C.POINTER(PE)]);snap=original.snapshot(2,0);original.check(snap,'private launch process inventory');p=PE();p.size=C.sizeof(p);rows=[]
 try:
  ok=first(snap,C.byref(p))
  while ok:
   if p.name.casefold()=='cross hermit.exe':
    h=original.openp(0x1000,False,p.pid)
    if h:
     try:
      name=C.create_unicode_buffer(32768);size=W.DWORD(len(name))
      if image_name(h,0,name,C.byref(size)) and Path(name.value).resolve()==APP.resolve():rows.append(dict(pid=p.pid,parent_pid=p.parent,image=name.value))
     finally:original.close(h)
   ok=nextp(snap,C.byref(p))
 finally:original.close(snap)
 return rows


def root_pid(rows):
 pids={r['pid'] for r in rows};roots=[r['pid'] for r in rows if r['parent_pid'] not in pids];need(len(roots)==1,'one fresh private process tree root');return roots[0]


def descendants(rows,root,known):
 selected={root}|set(known)
 for _ in range(len(rows)+1):
  following=selected|{r['pid'] for r in rows if r['parent_pid'] in selected}
  if following==selected:break
  selected=following
 return [r for r in rows if r['pid'] in selected]


class ToolLaunchedRuntime(original.OwnedOriginal):
 def __init__(self,request):
  super().__init__();self.request=Path(request);self.adopted=set();self.root_pid=None;self.launch_inventory=[]
 def adopt(self,rows):
  for row in rows:
   pid=row['pid']
   if pid in self.adopted:continue
   if pid in original.ids(self.job):self.adopted.add(pid);self.launch_inventory.append(dict(**row,adopted_elapsed=self.elapsed(),inherited_job=True));continue
   h=original.openp(0x1fffff,False,pid);original.check(h,'fresh private launch adoption handle')
   try:original.check(original.assign(self.job,h),'assign exact tool-launched private process to owned Job')
   finally:original.close(h)
   self.adopted.add(pid);self.launch_inventory.append(dict(**row,adopted_elapsed=self.elapsed()))
 def start(self):
  from tools.school_native_dialogue_desktop import require_unlocked
  self.desktop_preflight=require_unlocked()
  need(not private_processes(),'no preexisting private original process may be adopted');need(not self.request.exists(),'fresh tool launch request');need(sha(APP.read_bytes())==original.ORIGINAL_SHA,'source private executable identity')
  self.request.write_text(json.dumps(dict(status='request_tool_launch',app=str(APP.resolve()),original_sha256=original.ORIGINAL_SHA,preexisting_private_processes=[],started_wall_time_ns=time.time_ns())),encoding='utf8')
  deadline=time.monotonic()+60
  while time.monotonic()<deadline:
   rows=private_processes()
   if rows:
    self.root_pid=root_pid(rows);self.adopt(rows);root=self.root_pid;h=original.openp(0x1fffff,False,root);original.check(h,'actual tool-launched parent');self.pi.process=h;self.pi.pid=root;self.created=True;self.assigned=True
    tids=original.threads(root);need(tids,'actual parent thread for handle lifetime');self.pi.tid=tids[0];self.pi.thread=original.opent(0x100000,False,tids[0]);original.check(self.pi.thread,'actual parent thread handle');return
   time.sleep(.005)
  raise ValueError('tool did not launch the fresh private original within 60 seconds')
 def members(self):
  if self.root_pid:self.adopt(descendants(private_processes(),self.root_pid,self.adopted))
  return super().members()
 def finish(self):
  r=super().finish();r['launch_method']='computer-use sky.launch_app; actual fresh private tree adopted into owned Job';r['launch_inventory']=self.launch_inventory;return r
