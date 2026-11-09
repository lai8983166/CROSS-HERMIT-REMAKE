"""Narrow original opcode30 observation support over the frozen story verifier.

Authenticate the frozen verifier, change one explicit predicate in its AST, and
retain every other check and every raw sample. No VM bytes are normalized.
"""
import ast
import hashlib
from pathlib import Path
import struct
from devtools import terminal_menu_handoff_verification as parent

FROZEN_SHA='2936eb51f81d878188f3d03ec1de9602abd7b8bf9c8e0d462033de9119421240'
need=parent.need
word=parent.word


def contract(raw):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    parent.contract.authenticate(raw);md=Cs(CS_ARCH_X86,CS_MODE_32)
    checks={0x4CE9DD:('mov','word ptr [edx + ecx + 0x22], ax'),
        0x4CE9FB:('mov','word ptr [edx + ecx + 0x24], ax'),
        0x4CEDA2:('call','0x4c61c0'),0x4CEDAA:('jmp','0x4cfeb0'),
        0x4CFEF2:('mov','dword ptr [eax + edx + 0x1c], ecx'),
        0x4CFF0C:('mov','word ptr [edx + ecx + 0x20], ax')}
    for address,expected in checks.items():
        i=next(md.disasm(raw[address-0x400000:address-0x400000+15],address))
        need((i.mnemonic,i.op_str)==expected,'original opcode30 dispatch '+hex(address))
    need(word(raw,0x4D03CF-0x400000+(30-5)*4)==0x4CED8F,'original opcode30 table arm')


def check_dispatch(action,code):
    """code must already be bound to this live program by verify_program."""
    _,program,pc=action['key'];samples=action['samples'];new=[]
    advance=next((i for i,s in enumerate(samples)if word(bytes.fromhex(s['VM_hex']),28)!=pc),None)
    for index,s in enumerate(samples):
        if advance is not None and index>=advance:break
        vm=parent.blob(s['VM_hex'],128,'opcode30 sample')
        if struct.unpack_from('<H',vm,34)[0]!=30:continue
        need(0<=pc<=len(code)-20 and code[pc:pc+4]==bytes.fromhex('1e001400'),
             'opcode30 length20 at the authenticated original script PC')
        need(vm[4]!=0 and word(vm,16)==program and word(vm,28)==pc
             and struct.unpack_from('<HHH',vm,32)==(0,30,20),'exact original opcode30 in-flight fields')
        need(advance is not None and index<advance,'opcode30 has an observed subsequent advance')
        after=parent.blob(samples[advance]['VM_hex'],128,'opcode30 advanced sample')
        need(after[4]!=0 and word(after,16)==program and word(after,28)==pc+20
             and struct.unpack_from('<HHH',after,32)==(1,30,20),
             'original opcode30 exact length advance and resulting wait')
        new.append(dict(index=index,opcode=30,length=20,PC=pc,advanced_index=advance))
    return new


def adapted(adv):
    source=Path(parent.__file__).read_bytes()
    need(hashlib.sha256(source).hexdigest()==FROZEN_SHA,'fixed complete parent story verifier bytes')
    module=ast.parse(source.decode('utf8'));functions=[n for n in module.body if isinstance(n,ast.FunctionDef)and n.name=='verify_story_actions']
    need(len(functions)==1,'one fixed parent story function')
    fn=functions[0];count=0
    class ExpandOnePredicate(ast.NodeTransformer):
        def visit_Compare(self,node):
            nonlocal count
            if (isinstance(node.left,ast.Name)and node.left.id=='opcode'and len(node.ops)==1
                    and isinstance(node.ops[0],ast.Eq)and len(node.comparators)==1
                    and isinstance(node.comparators[0],ast.Constant)and node.comparators[0].value==40):
                count+=1
                return ast.copy_location(ast.Compare(left=node.left,ops=[ast.In()],
                    comparators=[ast.Tuple(elts=[ast.Constant(30),ast.Constant(40)],ctx=ast.Load())]),node)
            return self.generic_visit(node)
    fn=ExpandOnePredicate().visit(fn);need(count==1,'exactly one authenticated opcode40 predicate extended')
    tree=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]))
    scope=dict(parent.__dict__,ADV=adv)
    exec(compile(tree,__file__,'exec'),scope)
    return scope['verify_story_actions']


def verify(p,raw,game,hwnd,workers,maximum_allowed,adv,code_for_action):
    contract(raw)
    extra=[]
    for action in p['collector_story_input_actions']:
        extra.append(check_dispatch(action,code_for_action(action)))
    result=adapted(adv)(p,raw,game,hwnd,workers,maximum_allowed)
    need(len(result)==len(extra),'one raw story result per action')
    for row,addition in zip(result,extra):
        row['opcode30_original_dispatch_samples']=addition
    return result
