
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004f1510(int param_1)

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
  if (*(char *)(param_1 + 0x36) != '\0') {
    _local_c = CONCAT31(uStack_b,0x48);
    local_8 = param_1;
    if ((*(char *)(param_1 + 0x36) == '\x01') || (*(char *)(param_1 + 0x36) == '\x03')) {
      FUN__text__00505b90((int)_UNK_00752ba4,(int)_UNK_00752ba6,(int)_UNK_00752ba8,
                          (int)_UNK_00752baa,(int)_UNK_00752bac,(int)_UNK_00752bae,
                          (int)*(short *)(param_1 + 0xb6),(int)*(short *)(param_1 + 0xd0),
                          *(undefined1 *)(param_1 + 0x69),0x80,0x80,0x80,(int)_UNK_00752bb0,
                          (int)_UNK_00752bb2);
    }
    else {
      FUN__text__00505a60((int)_UNK_00752ba4,(int)_UNK_00752ba6,(int)_UNK_00752ba8,
                          (int)_UNK_00752baa,(int)_UNK_00752bac,(int)_UNK_00752bae,
                          (int)*(short *)(param_1 + 0xb6),(int)*(short *)(param_1 + 0xd0),
                          (int)_UNK_00752bb0,(int)_UNK_00752bb2);
    }
  }
  local_8 = 0x4f16ff;
  FUN__text__0056ce80();
  return;
}

