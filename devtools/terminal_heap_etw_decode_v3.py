"""Read one retained PID-heap ETL completely, without assuming its event version.

This is schema discovery, not heap-free acceptance. Every heap-provider event,
including foreign PIDs, is retained with native TDH metadata and property bytes.
The original v1/v2 capture implementations and their rejection remain unchanged.
"""
import argparse
import ctypes as C
import gzip
import hashlib
import json
from pathlib import Path, PureWindowsPath
import struct
import time
import uuid
from devtools import terminal_heap_etw_probe as parent

abi=parent.abi
need=parent.need
SOURCE_SHA='ea64989c04abfe59cb71216341192ec36025d3a312ec83754d48e9b96bc8c56a'
ETL_SHA='11ebdae815e9fa7d4c0e59e0e617af45268ea99b3f49f17ee44469067030792f'
PRODUCERS={
 'terminal_heap_etw_probe.py':(25594,'e7b4b12e007e72ba6fae6f1c1b9300f4dd9908776930a8e21b1686015463897b'),
 'terminal_heap_etw_probe_v2.py':(1293,'29c7fb18d030a07be26f55be4d2f0c158d0c48c031c868e4c09e9c689402670e'),
 'terminal_heap_etw_helper.cs':(3513,'48b71a742b57947e3c1f02d77acaeee7f59d5e289e63c911aabd92d933de3931'),
 'terminal_wait_etw_probe.py':(50506,'60af4a1e487fff1e738808804be36cf7223b2843a365b123b49b1784087a31f6')}
MAX_RECORDS=65536
MAX_RETAINED_BYTES=8*1024*1024


def identity(path):return parent.identity(Path(path))


def dependencies():
    return [identity(p)for p in (Path(__file__),Path(parent.__file__),Path(abi.__file__))]


def authenticate_source(path,sha,etl,etl_sha):
    source_id=identity(path);etl_id=identity(etl)
    need(sha==SOURCE_SHA==source_id['sha256']and 0<source_id['bytes']<=65536,'fixed original v2 source')
    need(etl_sha==ETL_SHA==etl_id['sha256']and etl_id['bytes']==262144,'fixed complete original v2 ETL')
    source=json.loads(Path(path).read_bytes())
    need(source['status']=='captured_decode_required'and not source['errors'],'source capture completed')
    need(all(source['ETL'][k]==etl_id[k]for k in ('bytes','sha256')),'ETL bound to original source')
    need(source['implementations']==source['implementations_after']and len(source['implementations'])==4,'unchanged original four producer identities')
    names=[PureWindowsPath(x['path']).name for x in source['implementations']]
    need(len(set(names))==4 and set(names)==set(PRODUCERS),'exact producer names')
    for row,name in zip(source['implementations'],names):
        actual=identity(Path(__file__).with_name(name));expected=PRODUCERS[name]
        need((row['bytes'],row['sha256'])==(actual['bytes'],actual['sha256'])==expected,'fixed capture producer '+name)
    parent.check_capture_source(source)
    parent.check_helper(source['helper']['ready'],source['helper']['live'],source['helper']['closed'])
    need(source['trace_stopped_before_live_cleanup']is True and source['cleanup']['helper_forced']is False
         and source['cleanup']['helper_exit']==0,'actual helper survived trace and cleaned up naturally')
    return source,source_id,etl_id


def utf16_at(raw,offset):
    need(type(offset)is int and 0<offset<len(raw) and offset%2==0,'bounded metadata UTF16 offset')
    end=offset
    while end+2<=len(raw) and end-offset<=512:
        if raw[end:end+2]==b'\0\0':return raw[offset:end].decode('utf-16-le')
        end+=2
    raise ValueError('bounded metadata string terminator absent')


def schema_fields(raw):
    need(112<=len(raw)<=65536,'complete bounded TRACE_EVENT_INFO')
    count,top=struct.unpack_from('<II',raw,100)
    need(0<=top<=count<=64 and 112+24*count<=len(raw),'bounded complete EVENT_PROPERTY_INFO array')
    fields=[]
    for i in range(top):
        at=112+i*24;flags,name_offset=struct.unpack_from('<II',raw,at)
        name=utf16_at(raw,name_offset);need(name and name not in [x['name']for x in fields],'unique actual top-level property')
        fields.append(dict(name=name,flags=flags,info_hex=raw[at:at+24].hex()))
    return fields


class EXTENDED_ITEM(C.Structure):
    _fields_=[('Reserved1',C.c_uint16),('ExtType',C.c_uint16),('Linkage',C.c_uint16),('DataSize',C.c_uint16),('DataPtr',C.c_uint64)]


def read_etl(path,source,result,deadline):
    result['ABI']=abi.decoder_layout();need(C.sizeof(EXTENDED_ITEM)==16 and EXTENDED_ITEM.DataPtr.offset==8,'native extended item ABI')
    api=C.WinDLL('advapi32',use_last_error=True);tdh=C.WinDLL('tdh',use_last_error=True)
    api.OpenTraceW.argtypes=[C.POINTER(abi.LOGFILE)];api.OpenTraceW.restype=C.c_uint64
    api.ProcessTrace.argtypes=[C.POINTER(C.c_uint64),C.c_uint32,C.c_void_p,C.c_void_p];api.ProcessTrace.restype=C.c_uint32
    api.CloseTrace.argtypes=[C.c_uint64];api.CloseTrace.restype=C.c_uint32
    tdh.TdhGetEventInformation.argtypes=[C.POINTER(abi.EVENT_RECORD),C.c_uint32,C.c_void_p,C.c_void_p,C.POINTER(C.c_uint32)]
    tdh.TdhGetEventInformation.restype=C.c_uint32
    tdh.TdhGetPropertySize.argtypes=[C.POINTER(abi.EVENT_RECORD),C.c_uint32,C.c_void_p,C.c_uint32,C.POINTER(abi.PROPERTY_DESCRIPTOR),C.POINTER(C.c_uint32)]
    tdh.TdhGetPropertySize.restype=C.c_uint32
    tdh.TdhGetProperty.argtypes=[C.POINTER(abi.EVENT_RECORD),C.c_uint32,C.c_void_p,C.c_uint32,C.POINTER(abi.PROPERTY_DESCRIPTOR),C.c_uint32,C.c_void_p]
    tdh.TdhGetProperty.restype=C.c_uint32
    schemas={};records=[];buffers=[];errors=[];counts={};digest=hashlib.sha256();total=0;retained_bytes=0;metadata_bytes=0;tdh_failures=0
    def schema(record):
        nonlocal metadata_bytes,tdh_failures
        h=record.contents.EventHeader;key=bytes(h.ProviderId).hex()+':'+bytes(h.EventDescriptor).hex()+':'+str(h.Flags&0x60)
        if key not in schemas:
            need(len(schemas)<64,'bounded complete schema inventory')
            row=dict(key=key,fields=[]);schemas[key]=row;size=C.c_uint32()
            status=int(tdh.TdhGetEventInformation(record,0,None,None,C.byref(size)));row['size_status']=status;row['requested_bytes']=size.value
            if status!=122 or not 112<=size.value<=65536:
                row['unavailable']='TDH metadata size/status';tdh_failures+=1;return row
            allocated=size.value;buf=C.create_string_buffer(allocated)
            status=int(tdh.TdhGetEventInformation(record,0,None,buf,C.byref(size)));row['read_status']=status
            if status!=0 or not 112<=size.value<=allocated:
                row['unavailable']='TDH metadata read/status';tdh_failures+=1;return row
            raw=buf.raw[:size.value];metadata_bytes+=len(raw);need(metadata_bytes<=512*1024,'bounded total TDH metadata')
            row.update(metadata_hex=raw.hex(),metadata_sha256=hashlib.sha256(raw).hexdigest(),provider_guid=str(uuid.UUID(bytes_le=raw[:16])),
                       event_guid=str(uuid.UUID(bytes_le=raw[16:32])),descriptor_hex=raw[32:48].hex())
            try:row['fields']=schema_fields(raw)
            except ValueError as exc:row['unavailable']=str(exc);tdh_failures+=1
        return schemas[key]
    def properties(record,meta):
        nonlocal tdh_failures
        out=[]
        for field in meta['fields']:
            row=dict(name=field['name']);out.append(row)
            # Structured/custom properties remain raw in metadata, never guessed.
            if field['flags']&(1|0x80):row['unavailable']='structured/custom property';tdh_failures+=1;continue
            name=C.create_unicode_buffer(field['name']);desc=abi.PROPERTY_DESCRIPTOR(C.cast(name,C.c_void_p).value,0xffffffff,0);size=C.c_uint32()
            status=int(tdh.TdhGetPropertySize(record,0,None,1,C.byref(desc),C.byref(size)));row.update(size_status=status,bytes=size.value)
            if status!=0 or size.value>256:row['unavailable']='bounded TDH property size/status';tdh_failures+=1;continue
            allocated=max(1,size.value);buf=C.create_string_buffer(allocated)
            status=int(tdh.TdhGetProperty(record,0,None,1,C.byref(desc),size.value,buf));row['read_status']=status
            if status!=0:row['unavailable']='TDH property read/status';tdh_failures+=1;continue
            row['hex']=buf.raw[:size.value].hex()
        return out
    def event(record):
        nonlocal total,retained_bytes
        if errors:return
        try:
            need(time.monotonic()<deadline,'bounded schema decode deadline');total+=1;need(total<=100000,'bounded complete ETL event count')
            e=record.contents;h=e.EventHeader
            need(e.UserDataLength<=65535 and (e.UserData or not e.UserDataLength),'valid bounded raw payload')
            payload=C.string_at(e.UserData,e.UserDataLength)if e.UserDataLength else b''
            need(e.ExtendedDataCount<=64 and (e.ExtendedData or not e.ExtendedDataCount),'bounded raw extended-data list')
            extended=[]
            if e.ExtendedDataCount:
                items=C.cast(e.ExtendedData,C.POINTER(EXTENDED_ITEM))
                for n in range(e.ExtendedDataCount):
                    item=items[n];need(item.DataPtr or not item.DataSize,'valid native extended-data pointer')
                    data=C.string_at(item.DataPtr,item.DataSize)if item.DataSize else b''
                    extended.append(dict(item_hex=bytes(item).hex(),type=item.ExtType,data_hex=data.hex()))
            digest.update(struct.pack('<I',len(payload))+bytes(h)+bytes(e.BufferContext)+payload)
            digest.update(struct.pack('<I',len(extended)))
            for x in extended:
                data=bytes.fromhex(x['data_hex']);digest.update(bytes.fromhex(x['item_hex'])+struct.pack('<I',len(data))+data)
            guid=str(uuid.UUID(bytes_le=bytes(h.ProviderId)))
            if guid!=parent.HEAP_GUID:return
            need(len(records)<MAX_RECORDS,'bounded complete heap record count')
            retained_bytes+=84+len(payload)+sum(16+len(bytes.fromhex(x['data_hex']))for x in extended)
            need(retained_bytes<=MAX_RETAINED_BYTES,'bounded complete heap raw retention')
            meta=schema(record)
            row=dict(index=total,pid=h.ProcessId,tid=h.ThreadId,FILETIME=h.TimeStamp,opcode=h.EventDescriptor.Opcode,version=h.EventDescriptor.Version,
                     target_pid=h.ProcessId==source['helper']['ready']['pid'],header_hex=bytes(h).hex(),buffer_context_hex=bytes(e.BufferContext).hex(),
                     payload_hex=payload.hex(),extended_data=extended,schema_key=meta['key'],TDH_properties=properties(record,meta))
            records.append(row);key=f"{h.ProcessId}:{h.EventDescriptor.Opcode}:{h.EventDescriptor.Version}"
            counts[key]=counts.get(key,0)+1
        except Exception as exc:errors.append(repr(exc))
    def buffer(log):
        try:
            need(time.monotonic()<deadline and len(buffers)<80,'bounded complete heap buffers')
            need(log.contents.EventsLost==0,'buffer-reported events lost');buffers.append(int(log.contents.BuffersRead));return 0 if errors else 1
        except Exception as exc:errors.append(repr(exc));return 0
    event_cb=C.WINFUNCTYPE(None,C.POINTER(abi.EVENT_RECORD))(event);buffer_cb=C.WINFUNCTYPE(C.c_uint32,C.POINTER(abi.LOGFILE))(buffer)
    log=abi.LOGFILE();log.LogFileName=str(path);log.ProcessTraceMode=0x10000000
    log.EventRecordCallback=C.cast(event_cb,C.c_void_p).value;log.BufferCallback=C.cast(buffer_cb,C.c_void_p).value
    handle=int(api.OpenTraceW(C.byref(log)));need(handle!=0xffffffffffffffff,'OpenTraceW failed')
    try:
        header=log.LogfileHeader;result['ETL_header_raw_hex']=bytes(header).hex()
        need(header.EventsLost==header.BuffersLost==0 and header.BuffersWritten==source['trace']['statistics']['BuffersWritten'],'same complete zero-loss header/stop')
        need(header.StartTime<=source['helper']['live']['begin_filetime']<=source['helper']['live']['end_filetime']<=header.EndTime
             <=source['trace']['stop_intervals'][0]['end_filetime']<=source['helper']['closed']['begin_filetime'],'actual ETL and helper timing envelope')
        handles=(C.c_uint64*1)(handle);status=int(api.ProcessTrace(handles,1,None,None))
        result.update(process_trace_status=status,callback_errors=errors,buffer_reads=buffers,total_records=total,
                      heap_records=len(records),target_heap_records=sum(x['target_pid']for x in records),foreign_heap_records=sum(not x['target_pid']for x in records),
                      PID_opcode_version_counts=counts,schema_count=len(schemas),TDH_unavailable_count=tdh_failures,
                      complete_record_digest=digest.hexdigest(),
                      digest_coverage='payload length + converted header80 + buffer4 + payload + extension count; each extended item16 + length + bytes. Runtime extension pointers are retained as observed, not portable identities.')
        need(status==0 and not errors and buffers and buffers[-1]==header.BuffersWritten,'complete ProcessTrace required; never accept partial events')
        return records,list(schemas.values())
    finally:
        result['close_trace_status']=int(api.CloseTrace(handle));need(result['close_trace_status']==0,'owned offline reader closed')


def packed(path,data,limit):
    raw=json.dumps(data,separators=(',',':')).encode();need(len(raw)<=32*1024*1024,'bounded complete diagnostic JSON')
    content=gzip.compress(raw,mtime=0);need(len(content)<=limit,'complete diagnostic artifact cap; never truncate')
    with Path(path).open('xb')as f:f.write(content)
    return identity(path)


def decode(source_path,source_sha,etl_path,etl_sha,out):
    parent.qualified();start=time.monotonic();out=parent.new_output(out);before=dependencies()
    source,sid,eid=authenticate_source(source_path,source_sha,etl_path,etl_sha)
    records_path=out.with_suffix('.records.json.gz');schemas_path=out.with_suffix('.schemas.json.gz')
    need(not records_path.exists()and not schemas_path.exists(),'new complete diagnostic sidecars')
    result=dict(kind='PID_heap_complete_schema_diagnostic',accepted=False,original_game=False,fullABI=False,PTDcleanup=False,
                alloc_free_capability_proved=False,live_negative_proved=False,caller_stack_proved=False,source=sid,ETL=eid,
                source_producer_implementations=source['implementations'],implementations=before,errors=[],
                timestamp_mode='ProcessTrace FILETIME conversion, no manual correction; original QPC bytes remain in the exact ETL',
                foreign_events_policy='retain every heap-provider record, no foreign PID discarded or relabeled',
                raw_schema_policy='actual header version and native TDH metadata retained; no version-zero parser substitution')
    try:
        rows,schemas=read_etl(Path(etl_path),source,result,start+30)
        result['records']=packed(records_path,dict(source=sid,ETL=eid,subject=source['helper']['ready'],records=rows),2*1024*1024)
        result['schemas']=packed(schemas_path,dict(source=sid,ETL=eid,schemas=schemas),256*1024)
        result['status']='complete_heap_schema_diagnostic_retained'
    except Exception as exc:result['errors'].append(repr(exc));result['status']='blocked'
    result['elapsed_seconds']=time.monotonic()-start;result['implementations_after']=dependencies()
    try:
        unused,after_source,after_etl=authenticate_source(source_path,source_sha,etl_path,etl_sha)
        need(after_source==sid and after_etl==eid and before==result['implementations_after']and result['elapsed_seconds']<=30,'source/ETL/decoder unchanged within budget')
    except Exception as exc:result['errors'].append(repr(exc));result['status']='blocked'
    parent.write_report(out,result);return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--decode',action='store_true',help='compatibility flag; this module is always offline-only')
    for k in ('source','source-sha','etl','etl-sha','out'):parser.add_argument('--'+k,required=True)
    args=parser.parse_args();result=decode(args.source,args.source_sha,args.etl,args.etl_sha,Path(args.out))
    print(json.dumps(dict(status=result['status'],errors=result['errors'],accepted=False)))
    return 1 if result['status']=='blocked'else 2


if __name__=='__main__':raise SystemExit(main())
