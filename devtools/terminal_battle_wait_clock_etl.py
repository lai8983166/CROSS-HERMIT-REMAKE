"""Raw-QPC view of the same whole ETL; no UTC calibration or row truncation."""
import ast
import inspect
import textwrap
import argparse
import gzip
import json
from devtools import terminal_battle_wait_etl_v2 as capacity
from devtools.terminal_battle_wait_etl_v2 import *


def raw_qpc(value):
    need(type(value)is int and value>0,'positive actual raw QPC tick');return value


def raw_decoder():
    need(hashlib.sha256(Path(parent.__file__).read_bytes()).hexdigest()==PARENT_SHA,'fixed full ETL reader')
    tree=ast.parse(textwrap.dedent(inspect.getsource(parent.decode_etl)));counts=dict(mode=0,fields=0,first=0)
    class ClockOnly(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Attribute) and node.targets[0].attr=='ProcessTraceMode' and isinstance(node.targets[0].value,ast.Name) and node.targets[0].value.id=='log':
                need(isinstance(node.value,ast.Constant)and node.value.value==0x10000000,'original EVENT_RECORD mode')
                node.value=ast.Constant(0x10001000);counts['mode']+=1
            return self.generic_visit(node)
        def visit_keyword(self,node):
            if node.arg=='ns':node.arg='qpc_ticks';counts['fields']+=1
            elif node.arg=='FILETIME':node.arg='qpc_ticks'
            return self.generic_visit(node)
        def visit_Subscript(self,node):
            if isinstance(node.slice,ast.Constant)and node.slice.value=='ns':node.slice.value='qpc_ticks'
            return self.generic_visit(node)
        def visit_Expr(self,node):
            if isinstance(node.value,ast.Call)and len(node.value.args)==2 and isinstance(node.value.args[1],ast.Constant)and node.value.args[1].value=='first native timestamp equals ETL StartTime; no local-time calibration':
                counts['first']+=1
                return ast.parse("need(first_ticks>0 and header['ReservedFlags']==1,'actual raw QPC clock declared by ETL; no UTC comparison')").body[0]
            return self.generic_visit(node)
    tree=ClockOnly().visit(tree);need(counts==dict(mode=1,fields=2,first=1),'only explicit raw clock mode and field names changed')
    ast.fix_missing_locations(tree);scope=dict(parent.__dict__,MAX_SELECTED=capacity.MAX_SELECTED,filetime_ns=raw_qpc)
    # Log-header StartTime/EndTime remain FILETIME. Its unchanged validator uses
    # the original module's FILETIME conversion, not this callback clock binding.
    exec(compile(tree,__file__,'exec'),scope);return scope['decode_etl']


def decode_etl(path,source,result,deadline,consume_records):
    result.update(timestamp_coordinate='raw QPC ticks; never converted to UTC',raw_timestamp_mode=True)
    try:return raw_decoder()(path,source,result,deadline,consume_records)
    finally:result['digest_coverage']='uint32 payload-length + raw-QPC EVENT_HEADER80 + BUFFER_CONTEXT4 + UserData, every ETL record'


def main():
    from devtools import terminal_battle_wait_verification as verification
    from devtools.isolated_windows_vm import identity
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('source','source-sha','etl','etl-sha','out'):p.add_argument('--'+key,required=True)
    p.add_argument('--diagnostic-only',action='store_true');p.add_argument('--school-source');a=p.parse_args()
    source_path=Path(a.source);etl_path=Path(a.etl);out=Path(a.out);packed=out.with_suffix('.records.json.gz')
    need(not out.exists()and not packed.exists(),'new raw-clock artifacts')
    sid,eid=identity(source_path),identity(etl_path)
    need(sid['sha256']==a.source_sha and sid['bytes']<=2*1024*1024 and eid['sha256']==a.etl_sha and eid['bytes']<64*1024*1024,'exact bounded source/ETL')
    with gzip.open(source_path,'rb')as f:raw=f.read(8*1024*1024+1)
    need(len(raw)<=8*1024*1024,'bounded source expansion');source=json.loads(raw)
    verification.source_contract(source,eid,True)
    paths=[Path(__file__),Path(capacity.__file__),Path(parent.__file__),Path(frozen.__file__),Path(verification.__file__)]
    before=[identity(q)for q in paths]
    result=dict(status='blocked',accepted=False,errors=[],source=sid,ETL=eid,new_native_capture=False,implementations=before)
    def consume(rows):
        raw=json.dumps(dict(source=sid,ETL=eid,subject=source['subject'],timestamp_coordinate='raw QPC ticks',records=rows),separators=(',',':')).encode()
        need(len(raw)<=128*1024*1024,'bounded complete raw record expansion');data=gzip.compress(raw,mtime=0)
        need(len(data)<=capacity.SELECTED_GZIP_LIMIT,'bounded complete raw records; no truncation')
        with packed.open('xb')as f:f.write(data)
        result['selected_records']=identity(packed)
        return dict(raw_records_only=True,accepted=False,wait_returns_verified=False)
    started=time.monotonic()
    try:
        decode_etl(etl_path,source,result,started+180,consume)
        result['status']='raw_clock_records_retained'
    except Exception as exc:result['errors'].append(repr(exc))
    finally:
        result['elapsed_seconds']=time.monotonic()-started
        result['implementations_after']=[identity(q)for q in paths]
        need(before==result['implementations_after'],'raw decoder unchanged')
        with out.open('x',encoding='utf8')as f:json.dump(result,f,indent=2)
    print(json.dumps({k:result.get(k)for k in ('status','errors','total_records','retained_subject_records')}))
    return 1 if result['errors']else 0


if __name__=='__main__':raise SystemExit(main())
