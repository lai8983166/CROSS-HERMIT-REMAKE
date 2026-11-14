"""Versioned native mutation-entry receipts. Build only; no launcher."""
import hashlib
import json
from pathlib import Path
import types
from devtools import terminal_display_native as parent

ROOT=parent.ROOT
INCLUDE=ROOT/'devtools/terminal_display_mutation.inc'
need,identity,replace=parent.need,parent.identity,parent.replace
PARENT_SHA='8b0ddb6a4fbe307a59e10983143891b9e76a2eebffb607f0c8b76182c7b1b7f3'
PARENT_INCLUDE_SHA='86717e372127ab020721fb1441460b77e126a55dde7b2539f003799d67f716bd'

def source():
    need(identity(parent.__file__)['sha256']==PARENT_SHA and identity(parent.INCLUDE)['sha256']==PARENT_INCLUDE_SHA,'fixed qualified v5 source')
    s=parent.source()
    s=replace(s,'U32 displayWindowGeneration=0;','U32 displayWindowGeneration=0;\nvoid displayMutationBegin(const Request &,U32,const char *,const void *,U32);\nstd::string displayMutationReceipt(U32);')
    s=replace(s,'  ++gfxAttempts;using F=HRESULT',
        '  displayMutationBegin(q,savedError,"presentation52",pp,52);\n  ++gfxAttempts;using F=HRESULT')
    s=replace(s,'  std::array<unsigned char,1536> after{};',
        '  if(set||restore)displayMutationBegin(q,savedError,"gamma1536",set?pointer(a[2]):gfxOriginalGamma.data(),1536);\n  std::array<unsigned char,1536> after{};')
    s=replace(s,'  using F=ULONG (STDMETHODCALLTYPE *)(void *);auto fn=',
        '  if(!add&&p.kind==GfxDevice&&p.refs==1)displayMutationBegin(q,savedError,"final_device_release",nullptr,0);\n  using F=ULONG (STDMETHODCALLTYPE *)(void *);auto fn=')
    s=replace(s,'  inputCursorRestored=false;',
        '  displayMutationBegin(q,savedError,"cursor_before36",&before,36);\n  inputCursorRestored=false;')
    s=replace(s,'  while(inputShowDelta){',
        '  displayMutationBegin(q,savedError,"cursor_restore36",&inputOriginal,36);\n  while(inputShowDelta){')
    s=replace(s,' Result r=gfxDispatch(q,guard,savedError);',
        ' Result r=gfxDispatch(q,guard,savedError);r.extras+=displayMutationReceipt(q.id);')
    s=replace(s,'Result inputReply=inputDispatch(q,guard,savedError);',
        'Result inputReply=inputDispatch(q,guard,savedError);inputReply.extras+=displayMutationReceipt(q.id);')
    s=replace(s,'Result dispatch(const Request &q) {',INCLUDE.read_text(encoding='utf8')+'\nResult dispatch(const Request &q) {')
    return s

def self_check():
    s=source();before=parent.source()
    for a,b in [('DWORD WINAPI WorkerDispatcher(void *parameter) {','DWORD WINAPI Reader(void *) {'),('DWORD WINAPI Reader(void *) {','\n} // namespace')]:
        need(before[before.index(a):before.index(b,before.index(a))]==s[s.index(a):s.index(b,s.index(a))],'frozen Reader and worker logic')
    return dict(native_executed=False,desktop_used=False,native_admission=False,parent=identity(parent.__file__),parent_include=identity(parent.INCLUDE),generator=identity(__file__),include=identity(INCLUDE),generated_source_sha256=hashlib.sha256(s.encode()).hexdigest(),event='NATIVE_MUTATION_BEGIN',maximum_events=32,
        operations=['GFX_CREATE_DEVICE','GFX_GAMMA_SET','GFX_GAMMA_RESTORE','GFX_RELEASE(final_device)','INPUT_CURSOR_POS','INPUT_SHOW_CURSOR','INPUT_CURSOR_RESTORE'],
        preservation='PTD116 and LastError restored and read back after event emission, before native leaf; full receipt on normal R. An entry event never claims HRESULT, mutation completion or resource release.',
        limits='same 32MiB total input,16MiB output,32768B transfer and100000 commands; no original argument/result/cleanup change')

def build(folder):
    # Reuse the frozen compiler recipe without rebinding or editing its module.
    namespace=dict(vars(parent),__file__=__file__,INCLUDE=INCLUDE,source=source,self_check=self_check)
    compiler=types.FunctionType(parent.build.__code__,namespace,'build',parent.build.__defaults__)
    r=compiler(folder);r.update(parent_generator=identity(parent.__file__),parent_include=identity(parent.INCLUDE),base_build_generator=identity(parent.__file__))
    (Path(folder)/'static-report.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');return r
