
void FUN__text__00450a60(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_GetDriveTypeA)(param_1);
  local_10 = FUN__text__0056ce80();
  local_c = 0x450ab5;
  FUN__text__0056ce80();
  return;
}

