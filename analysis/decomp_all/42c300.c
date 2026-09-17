
void FUN__text__0042c300(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0042c210();
  iVar1 = FUN__text__0042ae20(param_1);
  *local_8 = iVar1;
  if ((*local_8 != 0) && (iVar1 = FUN__text__0042c270(*local_8), iVar1 == 0)) {
    FUN__text__0042c210();
  }
  local_8 = (int *)0x42c375;
  FUN__text__0056ce80();
  return;
}

