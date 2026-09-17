
void FUN__text__004d1560(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  short local_18;
  short local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_2;
  local_10 = 0;
  local_14 = 1;
  for (local_18 = 1; local_18 < 0xc; local_18 = local_18 + 1) {
    if (local_10 < *(int *)(&DAT_007cf468 + local_18 * 0x124)) {
      local_10 = *(int *)(&DAT_007cf468 + local_18 * 0x124);
      local_14 = local_18;
    }
  }
  FUN__text__004c1f40(param_1,*(uint *)(param_2 + 4) >> 0x1c,*(uint *)(param_2 + 4) & 0xfffffff,
                      (int)local_14);
  local_8 = 0x4d162e;
  FUN__text__0056ce80();
  return;
}

