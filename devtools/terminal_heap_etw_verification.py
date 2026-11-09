"""Pure validation of one observed WOW64 helper heap capability.

All six actual native TDH schemas are authenticated. Foreign-header heap
statistics remain foreign-header records, with their separately checked payload
ProcessId. No original-game, caller-stack, full ABI or PTD claim is made.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path, PureWindowsPath
import struct
import uuid
from devtools import terminal_heap_etw_decode_v3 as reader

need=reader.need
ROOT=Path(__file__).resolve().parents[1]
REPORT_SHA='23420a10f683c145135cb36caae3e4452e90cee748c817c56490a404892a4e7b'
RECORDS_SHA='0ab457945075d0ac361a63234bcbec298ff5acee0f173d0839be3641c30fc3cd'
SCHEMAS_SHA='3ea4c968861c159cdbe09849e0be331c452c0c1f2b2ca2163cf6381d60e936f8'
READER_SHA='131749c8cd53d1eb5bd17081e073596b513af3b2c669066b71fcc68697bee860'
SCHEMAS={
 (43,2,64):('6e020e79a18512c3e60a0898b204d44786c274f211be622f5a9436f1b7de6d60',['HeapHandle']),
 (44,2,64):('e5f68df96963fd9608aa4156289ea404e99e76e7886bf6c4373e484f7c7a3aec',['HeapHandle']),
 (38,3,64):('19f880c9e29a6056cf89521887fe7439a29d5da21bb55018bd32aaebee0de5c3',
             ['HeapHandle','FreeSpace','CommittedSpace','ReservedSpace','HeapFlags','ProcessId','LargeUCRSpace','FreeListLength','UCRLength','AllocatedSpace']),
 (33,2,32):('976bfbaa9eb023e062a09a41f5fb5aaac3947276eced5c33f0b6ad66df00572d',['HeapHandle','AllocSize','AllocAddress','SourceId']),
 (36,2,32):('ffe62b02f3795fb01c743aa663b88ef412c31d1f4ebe8067f36999fd111fb996',['HeapHandle','FreeAddress','SourceId']),
 (32,3,32):('3d5a4de074ebf342a81c52ddcf9ac5bbd096e694a511f4e468a2e87a7aaf93e4',['HeapHandle','HeapFlags','ReservedSpace','CommittedSpace','AllocatedSpace'])}


def uint(value,maximum=0xffffffff):return type(value)is int and 0<=value<=maximum


def identify(path):return reader.identity(Path(path))


def load(path,sha,compressed=False):
    ident=identify(path);need(ident['sha256']==sha and 0<ident['bytes']<=2*1024*1024,'fixed bounded retained file')
    if compressed:
        with gzip.open(path,'rb')as f:raw=f.read(8*1024*1024+1)
        need(len(raw)<=8*1024*1024,'bounded complete diagnostic expansion')
    else:raw=Path(path).read_bytes()
    return json.loads(raw),ident


def validate_schemas(items):
    need(len(items)==6,'all six observed schemas retained');out={};shapes=set()
    for row in items:
        need(row['size_status']==122 and row['read_status']==0 and 'unavailable'not in row,'successful native TDH metadata')
        raw=bytes.fromhex(row['metadata_hex']);need(len(raw)==row['requested_bytes'],'complete TDH metadata bytes')
        sha=hashlib.sha256(raw).hexdigest();need(sha==row['metadata_sha256'],'raw TDH metadata digest')
        fields=reader.schema_fields(raw);need(fields==row['fields'],'original parsed metadata agrees')
        guid=uuid.UUID(reader.parent.HEAP_GUID).bytes_le
        need(raw[:16]==raw[16:32]==guid and row['provider_guid']==row['event_guid']==reader.parent.HEAP_GUID,'actual heap provider/event schema identity')
        desc=raw[32:48];need(row['descriptor_hex']==desc.hex(),'raw descriptor bytes')
        parts=row['key'].split(':');need(len(parts)==3 and parts[:2]==[guid.hex(),desc.hex()],'schema key raw identity')
        width=int(parts[2]);shape=(desc[5],desc[2],width)
        need(shape in SCHEMAS and shape not in shapes,'only explicitly supported observed opcode/version/width');shapes.add(shape)
        expected,names=SCHEMAS[shape]
        need(sha==expected and [f['name']for f in fields]==names,'fixed actual native schema and property names')
        for f in fields:
            info=bytes.fromhex(f['info_hex']);count,length=struct.unpack_from('<HH',info,16)
            need(f['flags']==0 and count==1 and length in (4,8),'actual scalar count/width without dynamic field guessing')
        need(row['key']not in out,'unique complete schema key');out[row['key']]=(row,fields)
    return out


def verify_objects(source,report,record_artifact,schema_artifact):
    reader.parent.check_capture_source(source)
    reader.parent.check_helper(source['helper']['ready'],source['helper']['live'],source['helper']['closed'])
    need(report['status']=='complete_heap_schema_diagnostic_retained' and not report['errors']and not report['callback_errors'],'complete successful diagnostic reader')
    need(report['process_trace_status']==report['close_trace_status']==0 and report['TDH_unavailable_count']==0,'complete read and native TDH without missing values')
    need(report['total_records']==349 and report['heap_records']==180 and report['schema_count']==6,'all actual events and schemas accounted')
    header=reader.abi.LOG_HEADER.from_buffer_copy(bytes.fromhex(report['ETL_header_raw_hex']))
    need(header.EventsLost==header.BuffersLost==0 and header.BuffersWritten==source['trace']['statistics']['BuffersWritten']==4
         and report['buffer_reads']==[1,2,3,4],'all four original zero-loss buffers consumed')
    live=source['helper']['live'];target=source['helper']['ready']['pid']
    need(header.StartTime<=live['begin_filetime']<=live['end_filetime']<=header.EndTime
         <=source['trace']['stop_intervals'][0]['end_filetime']<=source['helper']['closed']['begin_filetime'],'original trace stopped before negative allocation cleanup')
    for artifact in (record_artifact,schema_artifact):
        need(all(artifact['source'][k]==report['source'][k]and artifact['ETL'][k]==report['ETL'][k]==source['ETL'][k]
             for k in ('bytes','sha256')),'artifacts bind the same complete source and ETL')
    need(record_artifact['subject']==source['helper']['ready'],'raw sequence subject matches original helper')
    schemas=validate_schemas(schema_artifact['schemas']);rows=record_artifact['records']
    need(len(rows)==180,'no heap record omitted');counts=Counter();own=[];foreign=[];prior_index=0;prior_time=0;used=set()
    for row in rows:
        h=bytes.fromhex(row['header_hex']);payload=bytes.fromhex(row['payload_hex']);bc=bytes.fromhex(row['buffer_context_hex'])
        need(len(h)==80 and len(bc)==4 and h[24:40]==uuid.UUID(reader.parent.HEAP_GUID).bytes_le,'complete native heap header/buffer context')
        tid,pid=struct.unpack_from('<II',h,8);stamp=struct.unpack_from('<q',h,16)[0];flags=struct.unpack_from('<H',h,4)[0]
        need(all(uint(row[k])for k in ('pid','tid','opcode','version','index'))and type(row['FILETIME'])is int,'raw fields are actual integers')
        need((tid,pid,stamp,h[45],h[42])==(row['tid'],row['pid'],row['FILETIME'],row['opcode'],row['version']),'raw event owner, time, opcode and version agree')
        need(row['target_pid']is(pid==target),'foreign header identity retained without relabeling')
        need(prior_index<row['index']<=349 and prior_time<=stamp and header.StartTime<=stamp<=header.EndTime,'original unique increasing record/time order')
        prior_index=row['index'];prior_time=stamp
        cpu=struct.unpack_from('<H',bc)[0]if flags&0x200 else bc[0]
        need(cpu<header.NumberOfProcessors,'original bounded event CPU')
        key=h[24:40].hex()+':'+h[40:56].hex()+':'+str(flags&0x60)
        need(key==row['schema_key']and key in schemas,'event descriptor and pointer flags select actual TDH schema')
        used.add(key);schema,fields=schemas[key];props=row['TDH_properties']
        need(len(props)==len(fields)and [x['name']for x in props]==[f['name']for f in fields],'all ordered actual TDH properties present')
        data={};combined=b''
        for prop,field in zip(props,fields):
            length=struct.unpack_from('<H',bytes.fromhex(field['info_hex']),18)[0];value=bytes.fromhex(prop['hex'])
            need(type(prop['size_status'])is int and type(prop['read_status'])is int and prop['size_status']==prop['read_status']==0
                 and type(prop['bytes'])is int and prop['bytes']==length==len(value)and 'unavailable'not in prop,'native TDH scalar retrieval and exact width')
            combined+=value;data[prop['name']]=int.from_bytes(value,'little')
        need(combined==payload,'every raw payload byte equals the ordered native TDH properties')
        need(row['extended_data']==[],'this source has no heap-event extended stack data; unknown additions rejected')
        op=row['opcode'];counts[f"{pid}:{op}:{row['version']}"]+=1
        if pid!=target:
            need(op==38 and row['version']==3 and data['ProcessId']==target,'only authenticated target-payload snapshot statistics may have a foreign header PID')
            foreign.append(dict(index=row['index'],header_pid=pid,header_tid=tid,payload_process_id=data['ProcessId'],heap=data['HeapHandle']))
        else:
            need(op!=38,'all observed snapshot statistics keep their actual foreign emission identity')
        if op in (33,36):need(pid==target,'foreign alloc/free never accepted')
        if data['HeapHandle']==live['heap']:
            need(pid==target and tid==source['helper']['ready']['tid']and live['begin_filetime']<=stamp<=live['end_filetime'],'owned heap event within helper operation and exact PID/TID')
            own.append(dict(index=row['index'],opcode=op,FILETIME=stamp,properties=data))
    need(used==set(schemas)and dict(counts)==report['PID_opcode_version_counts'],'every schema/event classification accounted with no ignored unknown events')
    need(len(foreign)==report['foreign_heap_records']==4 and len(rows)-len(foreign)==report['target_heap_records']==176,'complete foreign and target record counts')
    need([x['opcode']for x in own]==[32,33,33,36],'one real heap creation, two allocations and exactly one free in owned heap')
    first,second,last=[x['properties']for x in own[1:]]
    need((first['AllocAddress'],first['AllocSize'])==(live['freed_address'],live['freed_size'])and
         (second['AllocAddress'],second['AllocSize'])==(live['live_address'],live['live_size'])and
         last['FreeAddress']==live['freed_address'],'exact helper allocation/free address and size receipts')
    need(not any(x['opcode']==36 and x['properties'].get('FreeAddress')==live['live_address']for x in own),'retained live allocation has no free event before stop')
    return dict(finite_owned_WOW64_heap_capability=True,alloc_free_events_verified=True,live_negative_verified=True,
        original_game=False,fullABI=False,fullstate=False,PTDcleanup=False,accepted=False,caller_stack_verified=False,
        helper_HeapFree_BOOL_observed=True,event_HeapFree_BOOL_present=False,source_total_events=349,all_heap_events_checked=180,
        all_TDH_schemas_checked=6,owned_heap_events=own,foreign_snapshot_statistics=foreign,
        foreign_emitter_is_controller_independently_proved=False,
        limitation='Foreign header PID is preserved; only its TDH ProcessId attributes the snapshot statistics to the target. This source has no independent controller-PID receipt. Heap-event matches plus helper BOOL do not prove original-game free ABI, caller stacks, TLS clearing or PTD cleanup.')


def verify_files(directory):
    directory=Path(directory);source_path=directory/'terminal-heap-capability-v2-20261109.json';etl=directory/'terminal-heap-capability-v2-20261109/trace.etl'
    source,sid,eid=reader.authenticate_source(source_path,reader.SOURCE_SHA,etl,reader.ETL_SHA)
    report,rid=load(directory/'terminal-heap-decode-v3-20261109.json',REPORT_SHA)
    records,recid=load(directory/'terminal-heap-decode-v3-20261109.records.json.gz',RECORDS_SHA,True)
    schemas,schid=load(directory/'terminal-heap-decode-v3-20261109.schemas.json.gz',SCHEMAS_SHA,True)
    for key,ident in (('source',sid),('ETL',eid),('records',recid),('schemas',schid)):
        need(all(report[key][k]==ident[k]for k in ('bytes','sha256')),'original decode reference '+key)
    need(report['implementations']==report['implementations_after']and len(report['implementations'])==3,'unchanged complete decoder dependency set')
    expected={'terminal_heap_etw_decode_v3.py':READER_SHA,'terminal_heap_etw_probe.py':reader.PRODUCERS['terminal_heap_etw_probe.py'][1],
              'terminal_wait_etw_probe.py':reader.PRODUCERS['terminal_wait_etw_probe.py'][1]}
    need({PureWindowsPath(x['path']).name for x in report['implementations']}==set(expected),'exact executed decoder files')
    for row in report['implementations']:
        name=PureWindowsPath(row['path']).name;actual=identify(Path(__file__).with_name(name))
        need(actual['sha256']==row['sha256']==expected[name]and actual['bytes']==row['bytes'],'exact executed decoder bytes')
    need(report['source_producer_implementations']==source['implementations'],'decoder authenticated original producer identities')
    result=verify_objects(source,report,records,schemas);result['references']=[sid,eid,rid,recid,schid];return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,default=ROOT/'.venv-audit/native-worker');p.add_argument('--out',required=True,type=Path);args=p.parse_args()
    need(not args.out.exists(),'new finite capability proof')
    files=[Path(__file__),Path(reader.__file__),Path(reader.parent.__file__),Path(reader.abi.__file__)]+[Path(__file__).with_name(n)for n in reader.PRODUCERS]
    files=list(dict.fromkeys(files));before=[identify(x)for x in files]
    result=verify_files(args.directory);result.update(kind='finite_owned_WOW64_heap_capability_verification',implementations=before,implementations_after=[identify(x)for x in files])
    need(before==result['implementations_after'],'pure verifier and authenticated producers unchanged')
    for ref in result['references']:need(identify(ref['path'])==ref,'source remains original bytes throughout verification')
    content=(json.dumps(result,indent=2)+'\n').encode();need(len(content)<=65536,'small finite capability proof')
    with args.out.open('xb')as f:f.write(content)
    print(json.dumps(dict(finite_owned_WOW64_heap_capability=True,accepted=False,original_game=False,PTDcleanup=False)));return 2


if __name__=='__main__':raise SystemExit(main())
