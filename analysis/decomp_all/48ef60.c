
/* WARNING: Removing unreachable block (ram,0x0048efee) */

void FUN__text__0048ef60(int param_1,int param_2)

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
  iVar1 = FUN__text__00469c60(param_1);
  if (iVar1 == 0) {
    iVar1 = FUN__text__004693b0(param_1);
    if (iVar1 != 0) goto LAB__text__0048f092;
    FUN__text__0046b0f0(param_1,1);
    FUN__text__0046b0b0(param_1,1);
    iVar1 = FUN__text__00469ad0(param_1);
    if (iVar1 != 0) goto LAB__text__0048efd5;
    *(undefined1 *)(*(int *)(param_1 + 600) + 0xa4) = *(undefined1 *)(param_2 + 6);
    iVar1 = FUN__text__00468eb0(param_1);
    if ((iVar1 != 0) && (iVar1 = FUN__text__0046a430(param_1), iVar1 != 0)) {
      FUN__text__0046d970(param_1);
    }
    iVar1 = FUN__text__0046a430(param_1);
    if (iVar1 != 0) {
      FUN__text__00475140(param_1);
    }
    FUN__text__0046b0f0(param_1,0);
    FUN__text__0046b0b0(param_1,0);
  }
  else {
LAB__text__0048efd5:
    FUN__text__00475270(param_1,0x15);
  }
  *(undefined1 *)(param_1 + 0x500) = *(undefined1 *)(param_2 + 6);
LAB__text__0048f092:
  local_8 = 0x48f09f;
  FUN__text__0056ce80();
  return;
}

