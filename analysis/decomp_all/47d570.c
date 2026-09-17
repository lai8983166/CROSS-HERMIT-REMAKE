
void FUN__text__0047d570(int param_1,int param_2)

{
  undefined2 uVar2;
  int iVar1;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_64;
  for (iVar3 = 0x18; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (param_2 == 0) {
    local_c = param_1 + 0x2f4;
  }
  else {
    local_c = param_1 + 0x3e0;
  }
  local_10 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                          (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_14 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  local_18 = (short)((int)((int)*(short *)(param_1 + 0x4d0) +
                          ((int)*(short *)(param_1 + 0x4d0) >> 0x1f & 0x1fU)) >> 5);
  local_1c = (short)((int)((int)*(short *)(param_1 + 0x4d2) +
                          ((int)*(short *)(param_1 + 0x4d2) >> 0x1f & 0xfU)) >> 4);
  if (((local_10 != local_18) || (local_14 != local_1c)) &&
     (iVar3 = FUN__text__00437d10(param_1), iVar3 == 0)) {
    FUN__text__00437d90(param_1,param_2);
    uVar2 = (undefined2)((uint)*(int *)(param_1 + 600) >> 0x10);
    local_24 = FUN__text__00437e40(CONCAT22(uVar2,local_10),local_14,local_18,
                                   CONCAT22(uVar2,local_1c),local_c,
                                   *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),param_2);
    local_20 = local_24;
    if (((local_24 != -2) && (local_24 != -1)) && (local_24 == 1)) {
      iVar3 = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                   (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      iVar1 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)
                   ) >> 4;
      local_10._0_1_ = (undefined1)iVar3;
      *(undefined1 *)(local_c + 0x1c) = (undefined1)local_10;
      local_14._0_1_ = (undefined1)iVar1;
      *(undefined1 *)(local_c + 0x1d) = (undefined1)local_14;
      local_14 = (short)iVar1;
      local_10 = (short)iVar3;
    }
  }
  local_8 = 0x47d722;
  FUN__text__0056ce80();
  return;
}

