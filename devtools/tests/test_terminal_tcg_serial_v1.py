import base64,json,socket,threading,time,unittest,xml.etree.ElementTree as ET
from devtools.terminal_tcg_serial_media_v3 import answer,seed_cmd
from devtools.terminal_tcg_serial_client_v3 import boot_utc,child_ok,Channel
class SerialTests(unittest.TestCase):
 def test_copy_only_media(self):
  root=ET.fromstring(answer());tags=[x.tag.split('}')[-1]for x in root.iter()]
  self.assertFalse(set(tags)&{'DiskConfiguration','ImageInstall','WillWipeDisk'})
  self.assertEqual(next(x.text for x in root.iter()if x.tag.endswith('}Path')),r'cmd.exe /d /c A:\SEED.CMD')
  cmd=seed_cmd();self.assertNotIn(bytes([7]),cmd);self.assertNotIn(b'format ',cmd.lower());self.assertNotIn(b'diskpart',cmd.lower())
  self.assertIn(b'if not "!COUNT!"=="1" goto fail',cmd)
 def test_initialization_seed_retains_windows_program(self):
  from devtools.terminal_tcg_serial_media_v3 import seed_cmd as third
  data=third();before=b'C:'+bytes([92])+b'Windows'+bytes([92])+b'system32'+bytes([92])+b'userinit.exe,'
  self.assertIn(b'if not "!ORIGINAL!"=="'+before+b'" goto fail',data)
  self.assertIn(b'/d "'+before+b'C:',data)
  self.assertIn(b'reg unload HKLM'+bytes([92])+b'CMF_SERIAL_SEED_V3',data)
  self.assertNotIn(b'Startup',data)
 def test_boot_exact_utc(self):
  raw='\r\nLastBootUpTime=20261112123045.123456+480\r\n'.encode()
  self.assertEqual(boot_utc(raw),'2026-11-12T04:30:45.1234560Z')
  self.assertEqual(boot_utc(raw.decode().encode('utf-16-le')),'2026-11-12T04:30:45.1234560Z')
  with self.assertRaises(ValueError):boot_utc(b'LastBootUpTime=')
 def test_cleanup_requires_every_handle_and_job(self):
  r=dict(exit_code=0,cleanup_ok=True,error=None,timed_out=False,output_limit_exceeded=False,job_assigned_before_resume=True,job_terminated=False,active_processes_after=0,handle_close={k:True for k in ('thread','pipe_write','stdin','process','pipe_read','job')})
  self.assertTrue(child_ok(r));r['exit_code']=1;self.assertFalse(child_ok(r));self.assertTrue(child_ok(r,True))
  r['handle_close'].pop('job');self.assertFalse(child_ok(r,True))
 def test_late_buffered_reply_rejected(self):
  from devtools.terminal_tcg_serial_client_v3 import Channel as NewChannel
  ch=NewChannel.__new__(NewChannel);ch.buf=b'{"seq":1}'+bytes([10])
  with self.assertRaises(TimeoutError):ch.line(time.monotonic()-1)
 def test_fragmented_serial_reply_and_deadline(self):
  a,b=socket.socketpair();ch=Channel.__new__(Channel);ch.s=a;ch.buf=b''
  try:
   b.sendall(b'{"seq":');b.sendall(b'1}\n');self.assertEqual(ch.line(time.monotonic()+1),{'seq':1})
   b.sendall(b'{"seq":');
   with self.assertRaises(TimeoutError):ch.line(time.monotonic()+.02)
   b.sendall(b'2}\n');self.assertEqual(ch.line(time.monotonic()+1),{'seq':2})
  finally:a.close();b.close()
if __name__=='__main__':unittest.main()
