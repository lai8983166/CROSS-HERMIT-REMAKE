
void FUN__text__00430b20(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00468e10(param_1);
  if (iVar1 != 0) {
    *(char *)(local_8 + 0x2ef34 + (uint)*(byte *)(*(int *)(param_1 + 600) + 0xa4)) =
         *(char *)(local_8 + 0x2ef34 + (uint)*(byte *)(*(int *)(param_1 + 600) + 0xa4)) + '\x01';
  }
  local_8 = 0x430b95;
  FUN__text__0056ce80();
  return;
}

