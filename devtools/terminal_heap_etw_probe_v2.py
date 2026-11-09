"""Path-normalizing adapter for the frozen first heap capability observer.

No capture, helper, ETW extension, decode or cleanup semantics are changed.
All four actual implementation files are bound before and after execution.
"""
from pathlib import Path
from types import FunctionType
from devtools import terminal_heap_etw_probe as parent

PARENT_SHA='e7b4b12e007e72ba6fae6f1c1b9300f4dd9908776930a8e21b1686015463897b'


def dependencies():
    p=Path(parent.__file__)
    parent.need(parent.identity(p)['sha256']==PARENT_SHA,'fixed first heap capability implementation')
    abi=Path(parent.abi.__file__)
    parent.need(parent.identity(abi)['sha256']==parent.ABI_SHA,'fixed previously audited ETW ABI module')
    return [parent.identity(x)for x in (p,Path(__file__),p.with_name('terminal_heap_etw_helper.cs'),abi)]


def clone(function,**bindings):
    scope=dict(function.__globals__);scope.update(bindings)
    result=FunctionType(function.__code__,scope,function.__name__,function.__defaults__,function.__closure__)
    result.__kwdefaults__=function.__kwdefaults__
    return result


run=clone(parent.run,dependencies=dependencies)
decode=clone(parent.decode,dependencies=dependencies)
main=clone(parent.main,run=run,decode=decode)


if __name__=='__main__':raise SystemExit(main())
