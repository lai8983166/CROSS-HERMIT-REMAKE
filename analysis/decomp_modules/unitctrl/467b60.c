
void __fastcall FUN__text__00467b60(int param_1)

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
  if ((*(char *)(param_1 + 0x108b48) == '\0') && (*(char *)(param_1 + 0x108b3a) != '\0')) {
    *(int *)(param_1 + 0x2e6f8) = *(int *)(param_1 + 0x2e6f8) + 1;
    local_8 = param_1;
    iVar1 = FUN__text__00415040(1);
    *(int *)(local_8 + 0x2e6f4) = *(int *)(local_8 + 0x2e6f4) - iVar1;
    if (*(int *)(local_8 + 0x2e6f4) < 0) {
      *(undefined4 *)(local_8 + 0x2e6f4) = 0;
    }
  }
  local_8 = 0x467c15;
  FUN__text__0056ce80();
  return;
}

