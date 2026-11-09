"""Defer only automatic focus until actual factory and ready captures return.

No capture, activation success, input, or factory evidence is synthesized. The
frozen FocusedRuntime performs its original focus logic after this read-only
gate; its original startup_activation receipts remain authoritative.
"""
import ast
from contextlib import contextmanager
import ctypes as C
import ctypes.wintypes as W
import hashlib
import inspect
import json
from pathlib import Path
import threading
from types import SimpleNamespace

from devtools import terminal_menu_handoff as menu

base=menu.base
need=base.need
MENU_SHA='154efedd03310eee9321c71dd975903ae432dca7f48b5db8ad51f82bc97e9079'
LIFETIME_SHA='9199bbd3a645b9a3886ca8309cd46be466582812beb396b1446d85c826deef9b'
RUN_SOURCE_SHA='ee9c9ea49f646c5ca2b674af7e5b47d548132d836c4ecb16f8daa1b81242ea79'
CAPTURE_SOURCE_SHA='539daf1fea919d27f81a971e32577c00b8572b6bf0ad5ab3544723daacb7df20'
_CAPTURE=base.original.capture
_LOCK=threading.Lock()


def require_qualified_guest():
    from devtools.native_input_isolation import require_qualified_guest as qualify
    return qualify()


def identity(path):
    path=Path(path);raw=path.read_bytes()
    return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def authenticate():
    rows=[identity(p)for p in (menu.__file__,base.original.__file__,__file__)]
    need(rows[0]['sha256']==MENU_SHA and rows[1]['sha256']==LIFETIME_SHA,
         'fixed original menu and factory observer source identities')
    need(hashlib.sha256(inspect.getsource(menu.run).encode()).hexdigest()==RUN_SOURCE_SHA and
         hashlib.sha256(inspect.getsource(_CAPTURE).encode()).hexdigest()==CAPTURE_SOURCE_SHA,
         'exact original run and capture function source')
    return rows


def handle_value(handle):
    value=getattr(handle,'value',handle)
    need(type(value)is int and value>0,'actual original process handle')
    return value


class FactoryFocusGate:
    """Per-scope state; only a complete original capture may open the gate."""
    def __init__(self,capture,window_owner):
        self.original_capture=capture;self.window_owner=window_owner
        self.captures={};self.active=True
        self.receipts=dict(schema_version=1,kind='factory_and_ready_before_automatic_focus',
            captures=[],focused_members_resumed=[],deferred_members_calls=0,
            host_game_calls=[],host_memory_writes=[],host_input_actions=[],
            activation_success_inferred=False,full_factory_trace_proved=False,accepted=False)

    def capture(self,h,pid,frames,g,elapsed,raw,objects=False):
        need(self.active,'factory focus capture scope still active')
        # The original capture must finish, including all reads, before any
        # marker is recorded. A throwing capture never opens the focus gate.
        result=self.original_capture(h,pid,frames,g,elapsed,raw,objects)
        need(isinstance(result,dict) and result['pid']==pid and result['frames']is frames,
             'unchanged original capture result and current process identity')
        factory=[f for f in result['frames']if
                 {0x49DF8A,0x45060F}<={r['return_va']for r in f['chain']}]
        loop=any(0x49DFD1<=f['EIP']<0x49E092 or any(
            0x49DFD1<=r['return_va']<0x49E092 for r in f['chain'])for f in result['frames'])
        ready=objects is True and loop
        if ready:
            need(result['window']['pid']==pid and result['main']['pointer']==g['0x7a4a00'] and
                 result['game']['pointer']==g['0x7a49fc'] and result['cache']['pointer']==g['0x80a398'] and
                 all(g[k]for k in ('0x7a4a00','0x7a49fc','0x80a398')),
                 'actual complete original ready objects for the same process')
        if factory or ready:
            key=(pid,handle_value(h))
            need(key in self.captures or len(self.captures)<4,'bounded original factory/ready identities')
            observed=self.captures.setdefault(key,{})
            for kind,condition in (('factory',bool(factory)),('ready',ready)):
                if not condition or kind in observed:continue
                data=json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
                receipt=dict(kind=kind,pid=pid,elapsed=result['elapsed'],capture_returned=True,
                    original_capture_sha256=hashlib.sha256(data).hexdigest(),original_capture_bytes=len(data),
                    factory_frame_tids=[f['tid']for f in factory]if kind=='factory'else [],
                    canonical_encoding='UTF-8 JSON sort_keys=True,separators=(comma,colon),ensure_ascii=False')
                observed[kind]=len(self.receipts['captures']);self.receipts['captures'].append(receipt)
        return result

    def deferred_runtime(self,focused):
        gate=self
        class DeferredRuntime(focused):
            def members(self):
                need(gate.active,'deferred runtime cannot outlive its capture scope')
                # Until both captures exist, skip exactly FocusedRuntime's
                # override, preserving the underlying original Job enumeration.
                possible={pid:proof for (pid,h),proof in gate.captures.items()
                    if 'factory'in proof and 'ready'in proof and pid in self.handles and
                    handle_value(self.handles[pid])==h}
                pid=gate.window_owner()if possible else None
                if pid not in possible:
                    gate.receipts['deferred_members_calls']+=1
                    return super(focused,self).members()
                proof=possible[pid]
                if not any(r['pid']==pid for r in gate.receipts['focused_members_resumed']):
                    gate.receipts['focused_members_resumed'].append(dict(pid=pid,elapsed=self.elapsed(),
                        factory_capture_index=proof['factory'],ready_capture_index=proof['ready'],
                        original_focused_members_dispatched=True,activation_success_claimed=False))
                return super().members()
        return DeferredRuntime


def window_owner():
    hwnd=base.original.findwindow(b'Cross Hermit',None)
    if not hwnd:return None
    pid=W.DWORD();base.original.ownerpid(hwnd,C.byref(pid))
    return pid.value


def adapted_run(gate):
    source,start=inspect.getsourcelines(menu.run)
    need(hashlib.sha256(''.join(source).encode()).hexdigest()==RUN_SOURCE_SHA,'fixed original menu run source')
    tree=ast.parse(''.join(source));count=0
    expected=ast.parse('FocusedRuntime if controller else base.VisibleOwnedRuntime',mode='eval').body
    class RuntimeOnly(ast.NodeTransformer):
        def visit_keyword(self,node):
            nonlocal count
            if node.arg=='VisibleOwnedRuntime':
                need(ast.dump(node.value)==ast.dump(expected),'exact original conditional focused runtime')
                node.value.body=ast.copy_location(ast.Call(func=ast.Name(id='_deferred_runtime',ctx=ast.Load()),
                    args=[ast.Name(id='FocusedRuntime',ctx=ast.Load())],keywords=[]),node.value.body)
                count+=1
            return node
    tree=RuntimeOnly().visit(tree);need(count==1,'one original FocusedRuntime selection only')
    ast.fix_missing_locations(tree);ast.increment_lineno(tree,start-1)
    namespace=dict(menu.run.__globals__,_deferred_runtime=gate.deferred_runtime)
    exec(compile(tree,menu.__file__,'exec'),namespace)
    return namespace['run']


@contextmanager
def scope():
    """Yield .menu_run and .receipts; the caller clones menu_run normally.

    All owned runtime use must finish before leaving this single-active scope.
    The only temporary module mutation is the original capture observer hook.
    """
    qualification=require_qualified_guest()
    need(_LOCK.acquire(blocking=False),'factory focus scope cannot overlap or reenter')
    gate=None;installed=None;before=None
    try:
        before=authenticate()
        need(base.original.capture is _CAPTURE,'original capture hook must be unmodified on entry')
        gate=FactoryFocusGate(_CAPTURE,window_owner)
        run=adapted_run(gate)
        gate.receipts['implementations']=before
        gate.receipts['qualification']=qualification
        installed=gate.capture
        base.original.capture=installed
        yield SimpleNamespace(menu_run=run,receipts=gate.receipts)
    finally:
        errors=[]
        if installed is not None:
            if base.original.capture is not installed:errors.append('capture hook changed inside factory focus scope')
            base.original.capture=_CAPTURE
            gate.active=False
            gate.receipts['capture_hook_restored']=base.original.capture is _CAPTURE
        try:
            if before is not None:
                after=authenticate()
                if gate is not None:gate.receipts['implementations_after']=after
                if before!=after:errors.append('factory focus implementation changed during scope')
        except BaseException as exc:errors.append('final factory focus identity check failed: '+repr(exc))
        finally:_LOCK.release()
        if gate is not None:gate.receipts['scope_errors']=errors
        need(not errors,'; '.join(errors))
