
void __thiscall FUN__text__00480640(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  local_c = (int *)(param_1 + 0xdccd8);
  local_8 = param_1;
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    if ((((*(short *)(param_2 + 2) != *(short *)(local_c[local_10 + 1] + 2)) &&
         (*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0xa4) ==
          *(char *)(*(int *)(param_2 + 600) + 0xa4))) &&
        (*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0x98) ==
         *(char *)(*(int *)(param_2 + 600) + 0x98))) &&
       (iVar1 = FUN__text__0046a120(local_c[local_10 + 1]), iVar1 != 0)) {
      local_14 = local_14 + 1;
    }
  }
  local_8 = 0x480739;
  FUN__text__0056ce80();
  return;
}

