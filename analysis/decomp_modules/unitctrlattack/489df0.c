
void FUN__text__00489df0(undefined4 param_1,int *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00427eb0();
  for (local_c = 0; local_c != *param_2; local_c = local_c + 1) {
    local_10 = FUN__text__00427d60();
    *(int *)(local_10 + 8) = param_2[local_c + 1];
    FUN__text__00427e30(local_10);
  }
  local_8 = 0x489e67;
  FUN__text__0056ce80();
  return;
}

