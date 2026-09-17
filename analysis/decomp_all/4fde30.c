
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004fde30(int param_1)

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
  local_8 = param_1;
  if (*(char *)(param_1 + 0x39) != '\0') {
    _local_c = CONCAT31(uStack_b,0x69);
    if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
      FUN__text__00505580((int)_UNK_00757790,(int)_UNK_00757792,(int)_UNK_00757794,
                          (int)_UNK_00757796,(int)_UNK_00757798,(int)_UNK_0075779a,
                          (int)_UNK_0075779c,(int)_UNK_0075779e,*(undefined1 *)(param_1 + 0x69),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_UNK_00757790,(int)_UNK_00757792,(int)_UNK_00757794,
                          (int)_UNK_00757796,(int)_UNK_00757798,(int)_UNK_0075779a,
                          (int)_UNK_0075779c,(int)_UNK_0075779e);
    }
  }
  if (*(char *)(local_8 + 0x3a) != '\0') {
    _local_c = CONCAT31(uStack_b,0x6a);
    if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
      FUN__text__00505580((int)_UNK_007577a0,(int)_UNK_007577a2,(int)_UNK_007577a4,
                          (int)_UNK_007577a6,(int)_UNK_007577a8,(int)_UNK_007577aa,
                          (int)_UNK_007577ac,(int)_UNK_007577ae,*(undefined1 *)(local_8 + 0x6a),0x80
                          ,0x80,0x80);
    }
    else {
      FUN__text__00505000((int)_UNK_007577a0,(int)_UNK_007577a2,(int)_UNK_007577a4,
                          (int)_UNK_007577a6,(int)_UNK_007577a8,(int)_UNK_007577aa,
                          (int)_UNK_007577ac,(int)_UNK_007577ae);
    }
  }
  local_8 = 0x4fe18d;
  FUN__text__0056ce80();
  return;
}

