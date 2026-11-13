"""Build-only texture persistence extension; no helper launcher."""
from pathlib import Path
import hashlib
from devtools import terminal_input_native as parent

ROOT=parent.ROOT
INCLUDE=ROOT/'devtools/terminal_texture_native.inc'
need,identity,replace=parent.need,parent.identity,parent.replace
OPS={'TEX_VERIFY':3}
PARENT_SHA='5b1976099e39749b61470e0727f42133ca47699892cf2bdff9eb62aaea2c5430'
PARENT_INCLUDE_SHA='d5929062e27df9e00b75ea4a73c1375242f4cb8f285685cf0c44235ccb4a0fe2'

def source():
    need(identity(parent.__file__)['sha256']==PARENT_SHA and identity(parent.INCLUDE)['sha256']==PARENT_INCLUDE_SHA,'frozen input native parent')
    s=parent.source()
    s=replace(s,'bool locked=false; };','bool locked=false; U32 generation=0,unlockedGeneration=0,verifiedGeneration=0; bool verifyPending=false; };\nU32 textureGeneration=0; bool textureFailed=false;')
    s=replace(s,'if(p.locked||p.width!=256','if(p.locked||p.verifyPending||p.width!=256')
    s=replace(s,'p.locked=true;p.pitch=v[0];','p.locked=true;p.generation=++textureGeneration;if(!p.generation)fatal(132);p.pitch=v[0];')
    s=replace(s,'" lock_bytes="+number(p.pitch*256);','" lock_bytes="+number(p.pitch*256)+" lock_generation="+number(p.generation);')
    s=replace(s,'p.locked=false;p.bits=0;p.format=26;}return r;',
      'p.verifyPending=p.format==26;p.unlockedGeneration=p.generation;p.locked=false;p.bits=0;p.format=26;r.extras="lock_generation="+number(p.generation)+" unlocked_generation="+number(p.unlockedGeneration)+" verification_required="+number(p.verifyPending);}return r;')
    s=replace(s,'if(!add&&(p.locked||','if(!add&&(p.locked||p.verifyPending||')
    s=replace(s,'Result dispatch(const Request &q) {',INCLUDE.read_text(encoding='utf8')+'\nResult dispatch(const Request &q) {')
    s=replace(s,'    if (inputOp(q.op)) return inputDispatch(q, guard, savedError);',
      '    if (q.op == "TEX_VERIFY") return textureVerify(q, guard, savedError);\n    if (inputOp(q.op)) return inputDispatch(q, guard, savedError);')
    s=replace(s,'r.extras = inputStatus()','r.extras = textureStatus() + " " + inputStatus()')
    s=replace(s,'if(inputGate || !inputEmpty()) return reject(',
      'if(textureFailed) return reject("SHUTDOWN_TEXTURE_VERIFICATION_FAILED", ERROR_BUSY);\n            if(inputGate || !inputEmpty()) return reject(')
    return s

def self_check():
    s=source();before=parent.source()
    for a,b in [('DWORD WINAPI WorkerDispatcher(void *parameter) {','DWORD WINAPI Reader(void *) {'),('DWORD WINAPI Reader(void *) {','\n} // namespace')]:
        need(before[before.index(a):before.index(b,before.index(a))]==s[s.index(a):s.index(b,s.index(a))],'frozen queue and worker retained')
    return dict(native_executed=False,desktop_used=False,native_admission=False,parent=identity(parent.__file__),parent_include=identity(parent.INCLUDE),generator=identity(__file__),include=identity(INCLUDE),generated_source_sha256=hashlib.sha256(s.encode()).hexdigest(),operations=OPS,logical_bytes=131072,row_bytes=512,rows=256,maximum_pitch=1024,readonly_flag=16,scope='Original writable unlock success only; original readonly unlock does not introduce an upload obligation. A new readonly lock and actual unlock are supplemental; padding is observed but excluded from logical pixel comparison.')
