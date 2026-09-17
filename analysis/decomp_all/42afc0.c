
void FUN__text__0042afc0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [15];
  undefined4 uStack_c;
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_DeleteFileA)(param_1);
  local_8 = FUN__text__0056ce80();
  uStack_c = 0x42b00a;
  FUN__text__0056ce80();
  return;
}

