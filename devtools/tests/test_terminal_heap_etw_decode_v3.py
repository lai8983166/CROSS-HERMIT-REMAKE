import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import time
import unittest
import uuid
from unittest.mock import patch
from devtools import terminal_heap_etw_decode_v3 as v


ROOT=Path(__file__).resolve().parents[2]


def metadata():
    raw=bytearray(112+24+len('Address\0'.encode('utf-16-le')))
    raw[0:16]=uuid.UUID(v.parent.HEAP_GUID).bytes_le
    raw[32+2]=2 # Actual metadata descriptor version remains two.
    struct.pack_into('<II',raw,100,1,1)
    struct.pack_into('<IIHHIHHI',raw,112,0,136,16,0,0,1,4,0)
    raw[136:]='Address\0'.encode('utf-16-le')
    return bytes(raw)


class HeapSchemaTests(unittest.TestCase):
    def test_actual_capture_and_independent_decoder_identity(self):
        w=ROOT/'.venv-audit/native-worker'
        source,sid,eid=v.authenticate_source(w/'terminal-heap-capability-v2-20261109.json',v.SOURCE_SHA,
            w/'terminal-heap-capability-v2-20261109/trace.etl',v.ETL_SHA)
        self.assertEqual(source['helper']['ready']['pid'],6092)
        self.assertEqual(len(source['implementations']),4)
        self.assertNotEqual(source['implementations'],v.dependencies())
        for row in v.dependencies():self.assertEqual(hashlib.sha256(Path(row['path']).read_bytes()).hexdigest(),row['sha256'])

    def test_unrequested_source_hash_is_not_accepted(self):
        w=ROOT/'.venv-audit/native-worker'
        with self.assertRaisesRegex(ValueError,'fixed original v2 source'):
            v.authenticate_source(w/'terminal-heap-capability-v2-20261109.json','0'*64,w/'terminal-heap-capability-v2-20261109/trace.etl',v.ETL_SHA)

    def test_metadata_not_rewritten_to_version_zero(self):
        raw=metadata();fields=v.schema_fields(raw)
        self.assertEqual(raw[34],2);self.assertEqual(fields[0]['name'],'Address')
        self.assertEqual(fields[0]['info_hex'],raw[112:136].hex())

    def test_out_of_bounds_metadata_rejected(self):
        for kind in ('offset','count','truncated','unterminated'):
            raw=bytearray(metadata())
            if kind=='offset':struct.pack_into('<I',raw,116,999999)
            elif kind=='count':struct.pack_into('<I',raw,100,65)
            elif kind=='truncated':raw=raw[:120]
            else:raw[-2:]=b'aa'
            with self.assertRaises(ValueError):v.schema_fields(raw)

    def test_guest_rejection_before_source_read_or_winapi(self):
        with patch.object(v.parent,'qualified',side_effect=ValueError('host denied')),patch.object(v,'authenticate_source')as auth:
            with self.assertRaisesRegex(ValueError,'host denied'):v.decode(None,None,None,None,Path('unused.json'))
            auth.assert_not_called()

    def test_reader_keeps_version2_and_foreign_pid_when_tdh_unavailable(self):
        calls=[];state={};keep=[]
        def fn(f):return f
        class API:pass
        api=API();tdh=API()
        def open_trace(address):
            log=C.cast(address,C.POINTER(v.abi.LOGFILE));state['log']=log
            log.contents.LogfileHeader.StartTime=100;log.contents.LogfileHeader.EndTime=300
            log.contents.LogfileHeader.BuffersWritten=1;return 77
        def process(*unused):
            log=state['log'];callback=C.WINFUNCTYPE(None,C.POINTER(v.abi.EVENT_RECORD))(log.contents.EventRecordCallback)
            for pid,opcode in ((999,38),(123,33),(123,36)):
                event=v.abi.EVENT_RECORD();event.EventHeader.ProviderId[:]=uuid.UUID(v.parent.HEAP_GUID).bytes_le
                event.EventHeader.ProcessId=pid;event.EventHeader.ThreadId=5;event.EventHeader.EventDescriptor.Version=2
                event.EventHeader.EventDescriptor.Opcode=opcode;event.EventHeader.Flags=0x20;event.EventHeader.TimeStamp=200
                payload=C.create_string_buffer(b'0123456789abcdef');keep.append(payload)
                event.UserData=C.addressof(payload);event.UserDataLength=16;callback(C.byref(event))
            log.contents.BuffersRead=1
            b=C.WINFUNCTYPE(C.c_uint32,C.POINTER(v.abi.LOGFILE))(log.contents.BufferCallback)
            self.assertEqual(b(log),1);return 0
        api.OpenTraceW=fn(open_trace);api.ProcessTrace=fn(process)
        api.CloseTrace=fn(lambda h:calls.append(('close',h))or 0)
        tdh.TdhGetEventInformation=fn(lambda *args:1168)
        tdh.TdhGetPropertySize=fn(lambda *args:1168);tdh.TdhGetProperty=fn(lambda *args:1168)
        source=dict(helper=dict(ready=dict(pid=123),live=dict(begin_filetime=150,end_filetime=250),closed=dict(begin_filetime=400)),
                    trace=dict(statistics=dict(BuffersWritten=1),stop_intervals=[dict(end_filetime=350)]))
        result={}
        with patch.object(C,'WinDLL',side_effect=lambda name,**kw:api if name=='advapi32'else tdh):
            rows,schemas=v.read_etl(Path('not-opened-by-mock.etl'),source,result,time.monotonic()+30)
        self.assertEqual(len(rows),3);self.assertEqual([r['version']for r in rows],[2,2,2])
        self.assertEqual([r['target_pid']for r in rows],[False,True,True]);self.assertEqual(result['foreign_heap_records'],1)
        self.assertEqual(result['TDH_unavailable_count'],3);self.assertEqual(calls,[('close',77)])
        self.assertTrue(all(s['size_status']==1168 for s in schemas));self.assertFalse(result.get('alloc_free_capability_proved',False))


if __name__=='__main__':unittest.main()
