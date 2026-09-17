
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00482210(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  float10 fVar3;
  undefined4 local_6c [16];
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  float local_1c;
  float local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_20 = (int)*(short *)(param_1 + 4);
  local_1c = ((float)local_20 / _DAT_0059c670) * _DAT_0059d91c;
  fVar3 = (float10)FUN__text__0056d9d4((double)local_1c);
  local_1c = (float)fVar3;
  for (local_c = 0; local_c != *(int *)(local_8 + 0x108b50); local_c = local_c + 1) {
    local_24 = (int)*(short *)(param_1 + 2);
    local_18 = (((_DAT_0059d918 / (float)*(int *)(local_8 + 0x108b50)) * (float)local_c +
                (float)local_24) / _DAT_0059c670) * _DAT_0059d91c;
    FUN__text__0056d9d4((double)local_18);
    local_28 = (int)*(short *)(param_1 + 8);
    local_10 = __ftol();
    FUN__text__0056d924((double)local_18);
    local_2c = (int)*(short *)(param_1 + 10);
    local_14 = __ftol();
    FUN__text__0046df90(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4),local_10,local_14,1);
  }
  local_8 = 0x482362;
  FUN__text__0056ce80();
  return;
}

