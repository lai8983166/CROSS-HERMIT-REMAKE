
void FUN__text__00431990(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__00431a60(param_2);
  local_10 = (int)*(short *)(param_1 + 0x360 + local_c * 2);
  local_14 = 0;
  local_18 = -1;
  local_1c = 0;
  for (local_20 = 0; local_20 != 4; local_20 = local_20 + 1) {
    if (local_14 <= *(short *)(param_1 + 0x360 + local_20 * 2)) {
      local_14 = (int)*(short *)(param_1 + 0x360 + local_20 * 2);
      local_18 = local_20;
      local_1c = local_1c + 1;
    }
  }
  local_8 = 0x431a5a;
  FUN__text__0056ce80();
  return;
}

