
void FUN__text__0046bcc0(int param_1,undefined4 param_2)

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
  FUN__text__00465040(param_1 + 0x48,param_2,(int)*(char *)(param_1 + 0x28a));
  *(undefined1 *)(param_1 + 4) = 0;
  *(undefined2 *)(param_1 + 10) = 0;
  local_8 = 0x46bd1b;
  FUN__text__0056ce80();
  return;
}

