
void FUN__text__00442ce0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0041ae70();
  local_10 = *(int *)(param_1 + 8);
  FUN__text__0041ab10();
  for (local_14 = 0; local_14 != 0x10; local_14 = local_14 + 1) {
    puVar2 = (undefined4 *)(local_10 + 0x14 + local_14 * 0x88);
    puVar3 = (undefined4 *)(local_c + local_14 * 0x88);
    for (iVar1 = 0x22; iVar1 != 0; iVar1 = iVar1 + -1) {
      *puVar3 = *puVar2;
      puVar2 = puVar2 + 1;
      puVar3 = puVar3 + 1;
    }
  }
  local_18 = FUN__text__0041aea0();
  FUN__text__0041aee0(local_18);
  FUN__text__0044b610();
  local_8 = 0x442daa;
  FUN__text__0056ce80();
  return;
}

