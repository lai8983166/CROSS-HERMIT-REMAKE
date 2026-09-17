
void FUN__text__00472770(int param_1)

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
  iVar1 = FUN__text__00468d10(param_1);
  if (((iVar1 != 0) && (*(short *)(*(int *)(param_1 + 600) + 0x16) < 1)) &&
     (*(char *)(param_1 + 0x290) != '\r')) {
    FUN__text__00475270(param_1,0xd);
  }
  local_8 = 0x4727e1;
  FUN__text__0056ce80();
  return;
}

