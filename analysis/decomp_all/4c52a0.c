
void __thiscall FUN__text__004c52a0(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_3;
  local_10 = (undefined4 *)(param_3 + 0xc);
  *(uint *)(param_1 + 0x7820) = *(uint *)(param_3 + 4) >> 0x1c;
  *(uint *)(param_1 + 0x7824) = *(uint *)(param_3 + 4) & 0xfffffff;
  local_8 = param_1;
  FUN__text__004c7cd0();
  local_14 = (uint)local_14._2_2_ << 0x10;
  while ((local_14 & 0xffff) < *(uint *)(local_c + 8)) {
    local_18 = *local_10;
    local_10 = local_10 + 1;
    local_1c = FUN__text__004c2120(*(undefined4 *)(local_8 + 0x18 + param_2 * 0x1c8),local_18);
    FUN__text__004c7f80(local_1c);
    local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
  }
  local_8 = 0x4c538c;
  FUN__text__0056ce80();
  return;
}

