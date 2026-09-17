
void FUN__text__0046bc20(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0046a0a0(param_1);
  if ((((iVar1 != 0) && (*(int *)(*(int *)(param_1 + 600) + 0x20) != 0x7fffffff)) &&
      (-1 < *(int *)(*(int *)(param_1 + 600) + 0x24))) &&
     (*(int *)(*(int *)(param_1 + 600) + 0x24) = *(int *)(*(int *)(param_1 + 600) + 0x24) + -1,
     *(int *)(*(int *)(param_1 + 600) + 0x24) == 0)) {
    FUN__text__00475370(param_1,0xc,0);
  }
  local_8 = 0x46bcb9;
  FUN__text__0056ce80();
  return;
}

