
void __thiscall FUN__text__004d64d0(int param_1,ushort param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  undefined4 local_28;
  uint local_24;
  uint local_20;
  undefined4 local_1c;
  ushort local_18;
  undefined2 uStack_16;
  uint local_14;
  int local_10;
  uint *local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 0x6410) = 0;
  *(ushort *)(param_1 + 0x6412) = param_2;
  *(undefined2 *)(param_1 + 10) = 0;
  local_c = *(uint **)(param_1 + 0x6420);
  local_10 = *(int *)(param_1 + 0x6420) + 4;
  local_14 = *local_c;
  if (local_14 < param_2) {
    param_2 = (short)local_14 - 1;
  }
  param_2 = param_2 << 1;
  _local_18 = CONCAT22(uStack_16,param_2);
  local_20 = CONCAT22(local_20._2_2_,*(undefined2 *)(local_10 + (uint)param_2 * 2));
  local_24 = CONCAT22(local_24._2_2_,
                      *(undefined2 *)(*(int *)(param_1 + 0x6420) + 6 + (uint)param_2 * 2));
  local_8 = param_1;
  FUN__text__004d60e0(param_3);
  local_1c = (uint)local_1c._2_2_ << 0x10;
  while ((local_1c & 0xffff) < (local_24 & 0xffff)) {
    local_28 = FUN__text__004c2120(*(undefined4 *)(local_8 + 0x641c),
                                   (local_20 & 0xffff) + (local_1c & 0xffff));
    FUN__text__004d6150(local_28);
    local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
  }
  if (*(short *)(local_8 + 10) < *(short *)(local_8 + 8)) {
    *(undefined2 *)(local_8 + 8) = *(undefined2 *)(local_8 + 10);
  }
  local_8 = 0x4d662e;
  FUN__text__0056ce80();
  return;
}

