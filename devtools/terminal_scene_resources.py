"""Bounded read-only resource diagnostics on the original scene-owner observer.

No input automation, texture copying, native return substitution or collector
patching. The default runtime is hidden. Importing this module calls no WinAPI;
only the explicit CLI/run entry starts the inherited exclusively owned lifetime.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import gzip
import hashlib
import json
import inspect
import marshal
from pathlib import Path
import struct
import types

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
MAX_READ_BYTES=4096
MAX_READ_CALLS=96
MAX_NODES=6
POISON={0xCCCCCCCC,0xCDCDCDCD,0xDDDDDDDD,0xFEEEFEEE,0xFFFFFFFF}
RESOURCE_RANGES=((0x40E210,0x40E29A),(0x40E330,0x40EA80),
    (0x407AD0,0x408127),(0x40DB90,0x40DEB5),(0x40DF20,0x40E000),
    (0x403620,0x4037EF),(0x403BD0,0x403D44),(0x407710,0x4077B6),
    (0x428A40,0x428B59),(0x56F420,0x56F805))


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(data):return hashlib.sha256(data).hexdigest()
def word(data,at=0):return struct.unpack_from('<I',data,at)[0]


class ResourceDependencyError(RuntimeError):
    pass


class Reader:
    """One paused sample's hard read budget; rejects bad pointers before backend."""
    def __init__(self,get,max_bytes=MAX_READ_BYTES,max_calls=MAX_READ_CALLS):
        self.get=get;self.max_bytes=max_bytes;self.max_calls=max_calls
        self.bytes=0;self.calls=0;self.records=[]

    @staticmethod
    def valid(pointer,size,alignment=1):
        return (type(pointer) is int and type(size) is int and 0<size<=0x1000000
                and 0x10000<=pointer<0x100000000 and pointer+size<=0x100000000
                and pointer%alignment==0 and not any(abs(pointer-p)<0x100 for p in POISON))

    def read(self,pointer,size,label,alignment=1):
        row=dict(label=label,pointer=pointer,bytes=size,status='invalid_pointer')
        self.records.append(row)
        if not self.valid(pointer,size,alignment) or size>4096:
            return row
        if self.calls>=self.max_calls or self.bytes+size>self.max_bytes:
            row['status']='budget';return row
        self.calls+=1;self.bytes+=size
        try:
            raw=self.get(pointer,size)
            if not isinstance(raw,(bytes,bytearray)) or len(raw)!=size:
                row['status']='short_read';return row
            row.update(status='readable',hex=bytes(raw).hex())
        except Exception as exc:
            row.update(status='unreadable',error=type(exc).__name__+': '+str(exc)[:160])
        return row

    def integer(self,pointer,label):
        row=self.read(pointer,4,label,4)
        return (word(bytes.fromhex(row['hex'])) if row['status']=='readable' else None),row


def raw_of(row):
    return bytes.fromhex(row['hex']) if row.get('status')=='readable' else None


def crt_header(reader,pointer,label):
    """VC6 image contract: user-20h, size+10h, block-use+14h (not reversed).

    A readable candidate is NOT proof the address is an allocation base. Only
    plausible header plus guard bytes is classified; never traverse its links.
    """
    row=reader.read(pointer-0x20 if type(pointer) is int else None,0x20,label+'.header',4)
    result=dict(candidate=row,allocation_base_proved=False)
    raw=raw_of(row)
    if raw is None:return result
    fields=dict(next=word(raw),previous=word(raw,4),file_pointer=word(raw,8),
        line=word(raw,12),data_size=word(raw,16),block_use=word(raw,20),request=word(raw,24),guard_hex=raw[28:32].hex())
    result['fields']=fields;result['all_DD']=raw==b'\xdd'*32
    plausible=(fields['guard_hex']=='fdfdfdfd' and (fields['block_use']&0xFFFF) in (0,1,2,3,4)
               and 0<fields['data_size']<=64*1024*1024 and fields['line']<10000000)
    result['plausible_debug_header']=plausible
    if plausible and fields['file_pointer']:
        name=reader.read(fields['file_pointer'],64,label+'.file_prefix')
        result['file_prefix']=name
        if raw_of(name) is not None:
            data=raw_of(name);result['file_prefix_text']=data.split(b'\0',1)[0].decode('utf-8',errors='replace')
            result['file_name_complete']=b'\0' in data
    return result


def descriptor(reader,pointer,label):
    record=reader.read(pointer,0x80,label+'.bytes',4)
    result=dict(pointer=pointer,record=record)
    raw=raw_of(record)
    if raw is None:return result
    result.update(texture=word(raw,0x2C),device=word(raw,0x28),surface=word(raw,0x30),
        sprite_flags=struct.unpack_from('<H',raw,0x58)[0],alternate_descriptor=word(raw,0x48),
        all_DD=raw==b'\xdd'*len(raw),CRT=crt_header(reader,pointer,label))
    # Never dereference COM texture pointers or copy GPU/texture pixel storage.
    return result


def capture_queue(reader,renderer,renderer_raw,preferred_bucket=None):
    count=word(renderer_raw,8);bucket_base=word(renderer_raw,0x10)
    result=dict(renderer=renderer,bucket_count=count,bucket_base=bucket_base,nodes=[],buckets=[],
                complete_graph=False,status='bounded_subset')
    if not 0<count<=4096:
        result['status']='invalid_bucket_count';return result
    if not Reader.valid(bucket_base,count*8,4):
        result['status']='invalid_bucket_base';return result
    indexes=[]
    for index in (preferred_bucket,count-1,0):
        if type(index) is int and 0<=index<count and index not in indexes:indexes.append(index)
    seen=set()
    for index in indexes:
        head=reader.read(bucket_base+8*index,8,'queue.bucket.'+str(index),4)
        result['buckets'].append(dict(index=index,record=head))
        raw=raw_of(head)
        if raw is None:continue
        pointer=word(raw)
        local=set()
        while pointer:
            if pointer in local or pointer in seen:
                result['status']='cycle_or_shared_node';return result
            if len(seen)>=MAX_NODES:
                result['status']='node_budget';return result
            seen.add(pointer);local.add(pointer)
            node=reader.read(pointer,0x5C,'queue.node',4)
            row=dict(pointer=pointer,bucket=index,record=node);result['nodes'].append(row)
            raw=raw_of(node)
            if raw is None:break
            row['type']=word(raw,4);row['next']=word(raw)
            if row['type']==1:
                row['descriptor']=descriptor(reader,word(raw,0x50),'queue.descriptor')
            pointer=row['next']
    return result


def frame_argument(reader,row,offset,label):
    return reader.integer(row['bp']+offset,label)


def collect_resources(c,frames,main_tid):
    reader=Reader(c.get);result=dict(schema_version=1,same_pause_as_owner_sample=True,
        fault_proved=False,all_heap_traversed=False,texture_pixels_read=False,records=reader.records)
    result['CRT_runtime_fill_bytes']=reader.read(0x7619CC,2,'CRT.runtime_fill_bytes')
    game,game_row=reader.integer(0x7A49FC,'game.global')
    result['game_pointer']=game_row
    main=next((f for f in frames if f['tid']==main_tid),None)
    if game is None or not Reader.valid(game,0x1090,4):
        result['status']='game_unreadable';return finish(result,reader)
    renderer=game+0x1058;renderer_row=reader.read(renderer,0x38,'renderer.head',4)
    result['renderer']=dict(pointer=renderer,record=renderer_row)
    chain=main['chain'] if main else []
    sites={r['return_va']:r for r in chain if r['return_va'] in (0x40E24A,0x40EA11,0x40E573,0x49E6DE)}
    result['active_frames']={hex(k):v for k,v in sites.items()}
    current={};result['current_call']=current
    if 0x40EA11 in sites:
        row=sites[0x40EA11]
        current['renderer_this'],current['renderer_this_raw']=frame_argument(reader,row,-4,'bind.this')
        current['texture_argument'],current['texture_argument_raw']=frame_argument(reader,row,8,'bind.texture_argument')
    if 0x40E24A in sites:
        row=sites[0x40E24A]
        for label,offset in (('device_argument',8),('stage_argument',12),('D3D_texture_argument',16)):
            current[label],current[label+'_raw']=frame_argument(reader,row,offset,'D3D.'+label)
    if 0x40E573 in sites:
        row=sites[0x40E573]
        for label,offset in (('draw_this',-4),('node_local',-8),('node_argument',8),('descriptor_local',-0x8C)):
            current[label],current[label+'_raw']=frame_argument(reader,row,offset,'draw.'+label)
        node=current.get('node_argument')
        if node is not None:
            node_row=reader.read(node,0x5C,'current.node',4)
            current['node']=dict(pointer=node,record=node_row)
            raw=raw_of(node_row)
            if raw is not None:
                current['node']['type']=word(raw,4)
                current['node']['descriptor']=descriptor(reader,word(raw,0x50),'current.descriptor')
    preferred=None
    if 0x49E6DE in sites:
        preferred,record=frame_argument(reader,sites[0x49E6DE],-12,'render.bucket_index')
        result['active_bucket_index']=record
    # Capture producer selection only when its original frame is actually active.
    result['producer_selections']=[]
    for frame in frames:
        producer_bp=None
        if 0x407AD0<=frame['EIP']<0x408127:producer_bp=frame['EBP']
        for row in frame['chain']:
            if row['return_va']==0x40810F:producer_bp=row['saved_bp'];break
        if producer_bp is not None:
            sprite,sr=reader.integer(producer_bp-4,'producer.sprite')
            node,nr=reader.integer(producer_bp-8,'producer.node')
            pr=dict(tid=frame['tid'],bp=producer_bp,sprite_raw=sr,node_raw=nr)
            if sprite is not None:
                d=descriptor(reader,sprite,'producer.sprite');pr['sprite']=d
                if 'sprite_flags' in d:
                    pr['selected_descriptor']=d['alternate_descriptor'] if d['sprite_flags']&0x80 else sprite
                    pr['selection_rule']='original408065 alternate when flags+58 &80, otherwise408070 sprite itself'
            result['producer_selections'].append(pr)
    rr=raw_of(renderer_row)
    if rr is not None:result['queue']=capture_queue(reader,renderer,rr,preferred)
    desc=current.get('node',{}).get('descriptor',{})
    current['descriptor_argument_link']=dict(
        descriptor_readable=raw_of(desc.get('record',{})) is not None,
        descriptor_from_node=desc.get('pointer'),descriptor_saved_local=current.get('descriptor_local'),
        saved_local_matches_node=(desc['pointer']==current['descriptor_local'])
            if 'pointer' in desc and current.get('descriptor_local') is not None else None,
        texture_field=desc.get('texture'),texture_argument=current.get('texture_argument'),
        texture_matches_argument=(desc['texture']==current['texture_argument'])
            if 'texture' in desc and current.get('texture_argument') is not None else None)
    # Strong failure only at the active original binding chain, with raw argument
    # agreement. Unreadable queued descriptors alone are not proof of this cause.
    texture=current.get('texture_argument')
    if ({0x40E24A,0x40EA11,0x40E573}.issubset(sites) and texture in POISON
            and current.get('D3D_texture_argument')==texture
            and current.get('renderer_this')==current.get('draw_this')==renderer
            and current.get('stage_argument')==0):
        result.update(fault_proved=True,status='invalid_original_resource_argument',
            fault=dict(kind='original_binding_argument_is_poison',value=texture,
                       original_call=0x40E244,original_resource_read=0x40EA05,
                       argument_raw_memory_preserved=True,exact_freeing_owner_proved=False,
                       descriptor_argument_link=current['descriptor_argument_link']))
    else:result['status']='bounded_resource_observation'
    return finish(result,reader)


def finish(result,reader):
    result['read_budget']=dict(bytes_requested=reader.bytes,calls=reader.calls,
        max_bytes=reader.max_bytes,max_calls=reader.max_calls,max_queue_nodes=MAX_NODES)
    return result


class OriginalProxy:
    def __init__(self,original,frozen):self.original=original;self.frozen=frozen
    def __getattr__(self,name):return getattr(self.original,name)


def clone(function,**replacements):
    return types.FunctionType(function.__code__,dict(function.__globals__,**replacements),
                              function.__name__,function.__defaults__,function.__closure__)


def make_sampler(base_sample,original,state,source_identity,post_sample_hook=None):
    def sample(c,owned,hwnd,main_tid,worker_tid,node,worker_exited=False):
        captured={}
        @contextmanager
        def frozen(h,pid,tids):
            with original.frozen(h,pid,tids) as frames:
                yield frames
                captured['resources']=collect_resources(c,frames,main_tid)
                if captured['resources']['fault_proved']:
                    try:captured['source_after']=source_identity(c)
                    except Exception as exc:captured['source_identity_error']=repr(exc)
        row=clone(base_sample,original=OriginalProxy(original,frozen))(
            c,owned,hwnd,main_tid,worker_tid,node,worker_exited)
        row['resources']=captured['resources']
        if captured['resources']['fault_proved']:
            state.update(failure_sample=row,source_after=captured.get('source_after'),
                         source_identity_error=captured.get('source_identity_error'))
            raise ResourceDependencyError('original renderer received poisoned resource argument; bounded diagnostic stop')
        if post_sample_hook is not None:
            # Both original threads have been resumed before any input handoff.
            result=post_sample_hook(c,owned,hwnd,row)
            if result is not None:row['post_sample_handoff']=result
        return row
    return sample


def source_contract(raw):
    need(sha(raw)==SOURCE_SHA,'original source identity')
    expected={0x40E244:'ff90f4000000',0x40EA05:'8b422c',0x408065:'894150',
        0x408070:'895150',0x56F4F2:'83e920',0x56F5CC:'8b4210',0x56F4FB:'8b4214'}
    for at,hex_value in expected.items():
        data=bytes.fromhex(hex_value);need(raw[at-0x400000:at-0x400000+len(data)]==data,'resource source operand '+hex(at))
    return dict(source_sha256=SOURCE_SHA,ranges=[dict(pointer=a,bytes=b-a,
        sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RESOURCE_RANGES],
        checked_instruction_hex={hex(a):v for a,v in expected.items()},
        CRT_header=dict(user_minus=32,file_offset=8,line_offset=12,data_size_offset=16,
                        block_use_offset=20,request_offset=24,guard_offset=28),
        CRT_fill_data=dict(pointer=0x7619CC,bytes=2,initial_image_hex=raw[0x3619CC:0x3619CE].hex(),
                           runtime_data_recorded_separately=True,live_value_compared_to_image=False),
        no_whole_heap_walk=True,no_resource_API_calls=True)


def build_run(base,runtime_class=None,post_sample_hook=None):
    """Explicit injection API for orchestration; defaults to original hidden Job.

    The caller owns any automatic-input orchestration. This adapter never asks
    for manual interaction, activates a window or injects input.
    """
    state={}
    extended_identity=clone(base.source_identity,RANGES=base.RANGES+RESOURCE_RANGES)
    sampler=make_sampler(base.bounded_sample,base.original,state,extended_identity,post_sample_hook)
    probe=clone(base.run_probe,bounded_sample=sampler,source_identity=extended_identity)
    def resource_probe(*args,**kwargs):
        state.clear();report=probe(*args,**kwargs)
        if 'failure_sample' in state:
            row=state['failure_sample'];row['index']=len(report['samples']);report['samples'].append(row)
            report['resource_failure']=row['resources']['fault']
            report['stop_reason']='first_proved_invalid_original_resource_argument'
            if state.get('source_after') is not None:report['source_after']=state['source_after']
            if state.get('source_identity_error'):report['resource_source_after_error']=state['source_identity_error']
        return report
    runtime_class=runtime_class or base.native.OwnedRuntime
    run=clone(base.run,run_probe=resource_probe,VisibleOwnedRuntime=runtime_class)
    def execute(output,duration):
        base_path=Path(base.__file__);adapter_path=Path(__file__)
        base_before=sha(base_path.read_bytes());adapter_before=sha(adapter_path.read_bytes())
        hook_identity=None;hook_path=None
        if post_sample_hook is not None:
            hook_function=getattr(post_sample_hook,'__func__',post_sample_hook)
            need(isinstance(hook_function,types.FunctionType),'explicit Python post-sample hook')
            source_file=inspect.getsourcefile(hook_function)
            hook_path=Path(source_file).resolve() if source_file else None
            hook_identity=dict(module=hook_function.__module__,qualname=hook_function.__qualname__,
                code_sha256=sha(marshal.dumps(hook_function.__code__)),
                bound_method=hasattr(post_sample_hook,'__func__'),
                source_path=str(hook_path) if hook_path else None,
                source_sha256=sha(hook_path.read_bytes()) if hook_path and hook_path.is_file() else None,
                invoked_after_original_threads_resumed=True)
        contract=source_contract(base.SOURCE.read_bytes())
        result=run(output,duration)
        need(sha(base_path.read_bytes())==base_before and sha(adapter_path.read_bytes())==adapter_before,
             'observer implementations changed during native lifetime')
        if hook_identity and hook_identity['source_sha256']:
            need(sha(hook_path.read_bytes())==hook_identity['source_sha256'],'post-sample hook source changed during lifetime')
        result.update(kind='actual_same_owner_scene_resource_observation',accepted=False,
            resource_adapter=dict(path=str(adapter_path),sha256=adapter_before,base_path=str(base_path),
                base_sha256=base_before,cloned_functions=['bounded_sample','source_identity','run_probe','run'],
                runtime_class=runtime_class.__module__+'.'+runtime_class.__qualname__,
                source_contract=contract,input_automation_performed_by_adapter=False,manual_input_required=False,
                post_sample_hook=hook_identity,
                game_memory_written=False,original_renderer_return_substituted=False,
                max_extra_read_bytes_per_sample=MAX_READ_BYTES,max_extra_reads_per_sample=MAX_READ_CALLS),
            resource_status='failure' if (result.get('probe') or {}).get('resource_failure') else 'partial',
            full_resource_lifetime_proved=False,full_battle_exit_accepted=False)
        return result
    return execute


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--seconds',type=int,default=30)
    args=p.parse_args();out=args.out.resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh local output')
    need(1<=args.seconds<=600,'bounded native lifetime')
    from devtools import terminal_scene_owner as base
    result=build_run(base)(out,args.seconds)
    raw=json.dumps(result,separators=(',',':')).encode()
    need(len(raw)<=64*1024*1024,'bounded resource report')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=12*1024*1024,'compressed resource evidence budget')
    with out.open('xb') as stream:stream.write(packed)
    print(json.dumps(dict(path=str(out),bytes=len(packed),sha256=sha(packed),status=result['resource_status'],accepted=False)))
    if (result.get('probe') or {}).get('error') or result['lifecycle']['error']:raise SystemExit(1)


if __name__=='__main__':main()
