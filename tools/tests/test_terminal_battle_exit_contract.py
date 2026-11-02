import copy,struct,unittest
from unittest.mock import patch
from tools import terminal_battle_exit_contract as c
from tools import terminal_battle_exit_pixels as p

class ContractTests(unittest.TestCase):
 def row(self,name='neutral_running'):
  frames=[];segments=[]
  for i in range(349):
   frames.append(dict(index=i,segments=[i,i+1]))
   segments.append(dict(entry=0x454CF0,label='task_'+str(i),root=dict(receiver=c.TASK,args=[]),stop=c.RETURN,CPU=dict(EIP=c.RETURN,ESP=c.STACK+0xF004)))
  return dict(input=dict(name=name),terminal_battle_stage_handoff=dict(frames=frames,segments=segments))
 def test_task_count_includes_every_added_complete_original_task(self):
  self.assertEqual(c.parent_task_accounting(self.row())['complete_tasks'],1111)
  self.assertEqual(c.parent_task_accounting(self.row('timeout_before_combat'))['complete_tasks'],1138)
 def test_missing_task_is_not_silently_accepted(self):
  row=self.row();row['terminal_battle_stage_handoff']['segments'].pop()
  with self.assertRaises(ValueError):c.parent_task_accounting(row)
 def test_pending_task_is_not_counted_as_completed(self):
  row=self.row();row['terminal_battle_stage_handoff']['segments'][-1]['CPU']['EIP']=0x454CF0
  with self.assertRaises(ValueError):c.parent_task_accounting(row)
 def test_wrong_task_receiver_is_rejected(self):
  row=self.row();row['terminal_battle_stage_handoff']['segments'][2]['root']['receiver']=c.TASK+4
  with self.assertRaises(ValueError):c.parent_task_accounting(row)
 def test_duplicate_frame_accounting_rejected(self):
  row=self.row();row['terminal_battle_stage_handoff']['frames'][-1]['index']=0
  with self.assertRaises(ValueError):c.parent_task_accounting(row)
 def text(self):
  rows=[]
  for i in range(349):
   rows.append(dict(name='ImmGetOpenStatus',entry=0x76182A80,import_slot=0x5920EC,caller=0x425C99,args=[0],result=0,segment='input_'+str(i),actual_API_executed=True))
   rows.append(dict(name='lstrlenA',entry=0x770206E0,import_slot=0x5922C4,caller=0x425A7E,args=[c.INPUT+0x528],result=0,string_hex='',segment='task_'+str(i),actual_API_executed=True))
  return dict(terminal_battle_stage_handoff=dict(text_APIs=rows))
 def test_strict_parent_text_endpoints(self):self.assertEqual(c.strict_parent_text(self.text())['string_calls'],349)
 def test_unexpected_string_caller_buffer_or_bytes_rejected(self):
  for field,value in [('caller',0x400123),('args',[c.INPUT+0x529]),('string_hex','41'),('result',1),('actual_API_executed',False)]:
   row=self.text();row['terminal_battle_stage_handoff']['text_APIs'][1][field]=value
   with self.subTest(field=field),self.assertRaises(ValueError):c.strict_parent_text(row)
 def test_original_exit_instructions_and_wait_boundary(self):
  d=c.original_exit_contract();self.assertEqual(d['wait_return_address'],0x453CB5);self.assertFalse(d['terminal_battle_exit_executed'])
 def test_modified_original_exit_call_rejected(self):
  raw=bytearray(c.CODE);raw[0x453CB0-0x400000]=0x90
  with patch.object(c,'CODE',bytes(raw)),self.assertRaises(ValueError):c.original_exit_contract()
 def test_original_palette_instructions(self):self.assertTrue(p.original_palette_contract()['full_native_pitch_padding_retained'])
 def bitmap(self):
  data=bytearray(54+1024+8);data[:2]=b'BM';struct.pack_into('<I',data,10,1078);struct.pack_into('<iiHHI',data,18,3,2,1,8,0)
  data[54:58]=bytes([1,2,3,0]);data[58:62]=bytes([1,2,3,0]);data[62:66]=bytes([0,0,248,0]);data[66:70]=bytes([0,248,0,0])
  data[1078:]=bytes([2,3,0,1,3,2,1,0]);return bytes(data)
 def test_palette_key_and_bottom_up_conversion_preserve_actual_padding(self):
  before=bytes([0xA5])*48;out=p.indexed_bmp_image(self.bitmap(),0,before,12,4,4)
  self.assertEqual(struct.unpack_from('<4H',out,0),(0x83E0,0xFC00,0,0))
  self.assertEqual(struct.unpack_from('<4H',out,12),(0xFC00,0x83E0,0,0))
  self.assertEqual(out[8:12],before[8:12]);self.assertEqual(out[20:],before[20:])
 def test_opaque_mode_keeps_nonzero_duplicate_palette0(self):
  out=p.indexed_bmp_image(self.bitmap(),0,bytes(48),12,4,4,transparency=0)
  self.assertEqual(struct.unpack_from('<H',out,4)[0],0x8000)
 def test_bad_palette_or_native_span_rejected(self):
  with self.assertRaises(ValueError):p.indexed_bmp_image(self.bitmap()[:100],0,bytes(48),12,4,4)
  with self.assertRaises(ValueError):p.indexed_bmp_image(self.bitmap(),0,bytes(47),12,4,4)

 def test_original_loader_changes_black_palette_before_transparent_conversion(self):
  raw=bytearray(self.bitmap());struct.pack_into('<I',raw,46,4);raw[54:58]=bytes([0,0,248,0]);raw[58:62]=bytes(4)
  changed=p.bitmap_loader_palette(bytes(raw),0,1)
  self.assertEqual(changed[58:62],changed[54:58]);self.assertEqual(bytes(raw)[58:62],bytes(4))
  out=p.indexed_bmp_image(changed,0,bytes(48),12,4,4)
  self.assertEqual(struct.unpack_from('<H',out,4)[0],0)
 def test_zero_declared_palette_count_does_not_expand_to256(self):
  raw=bytearray(self.bitmap());struct.pack_into('<I',raw,46,0);struct.pack_into('<I',raw,10,54+65*4);raw[58:62]=bytes(4)
  out=p.bitmap_loader_palette(bytes(raw),0,1)
  self.assertEqual(struct.unpack_from('<I',out,46)[0],65)
  self.assertEqual(out[58:62],out[54:58])
  self.assertEqual(struct.unpack_from('<I',raw,46)[0],0)

if __name__=='__main__':unittest.main()
