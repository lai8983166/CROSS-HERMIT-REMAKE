
void __thiscall FUN__text__004d62f0(int param_1,short param_2,short param_3,undefined2 param_4)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  short local_18;
  short local_14;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(short *)(param_1 + 0x6410) == 0) {
    *(undefined2 *)(param_1 + 0x6410) = 1;
  }
  else {
    local_10 = local_10 & 0xffff0000;
    local_14 = param_2;
    local_18 = param_3;
    local_c = local_c & 0xffff0000;
    local_8 = param_1;
    while ((int)(local_c & 0xffff) < (int)*(short *)(local_8 + 8)) {
      uVar1 = (short)local_c + *(short *)(local_8 + 4);
      local_10 = CONCAT22(local_10._2_2_,uVar1);
      if ((int)*(short *)(local_8 + 10) <= (int)(uint)uVar1) break;
      *(undefined2 *)(local_8 + 0x82 + (uint)uVar1 * 0x80) = param_4;
      FUN__text__00408f90((int)local_14,(int)local_18);
      local_18 = local_18 + *(short *)(local_8 + 0x4e + (local_10 & 0xffff) * 0x80);
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
  }
  local_8 = 0x4d640c;
  FUN__text__0056ce80();
  return;
}

