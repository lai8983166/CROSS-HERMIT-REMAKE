
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004f1080(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined1 local_c;
  undefined3 uStack_b;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0xea) != '\0') {
    local_8 = param_1;
    if (*(char *)(param_1 + 0xea) == '\x01') {
      local_c = 0x13;
      FUN__text__00505580((int)_UNK_00752434,(int)_UNK_00752436,(int)_UNK_00752438,
                          (int)*(short *)(param_1 + 0x11a),(int)_UNK_0075243c,(int)_UNK_0075243e,
                          (int)_UNK_00752440,(int)_UNK_00752442,*(undefined1 *)(param_1 + 0x102),
                          0x80,0x80,0x80);
      _local_c = CONCAT31(uStack_b,0x14);
      FUN__text__00505580((int)_UNK_00752444,(int)_UNK_00752446,(int)_UNK_00752448,
                          *(short *)(local_8 + 0x11a) + -0x400,(int)_UNK_0075244c,(int)_UNK_0075244e
                          ,(int)_UNK_00752450,(int)_UNK_00752452,*(undefined1 *)(local_8 + 0x102),
                          0x80,0x80,0x80);
    }
    else {
      local_c = 0x13;
      FUN__text__00505000((int)_UNK_00752434,(int)_UNK_00752436,(int)_UNK_00752438,
                          (int)*(short *)(param_1 + 0x11a),(int)_UNK_0075243c,(int)_UNK_0075243e,
                          (int)_UNK_00752440,(int)_UNK_00752442);
      _local_c = CONCAT31(uStack_b,0x14);
      FUN__text__00505000((int)_UNK_00752444,(int)_UNK_00752446,(int)_UNK_00752448,
                          *(short *)(local_8 + 0x11a) + -0x400,(int)_UNK_0075244c,(int)_UNK_0075244e
                          ,(int)_UNK_00752450,(int)_UNK_00752452);
    }
  }
  local_8 = 0x4f1399;
  FUN__text__0056ce80();
  return;
}

