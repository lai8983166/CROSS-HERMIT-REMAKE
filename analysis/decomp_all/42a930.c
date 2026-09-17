
void FUN__text__0042a930(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_14c [16];
  undefined4 local_10c;
  undefined1 local_108 [244];
  undefined4 uStack_14;
  
  puVar2 = local_14c;
  for (iVar1 = 0x52; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_lstrcpyA)(local_108,param_1);
  FUN__text__0056ce80();
  FUN__text__004297e0(local_108);
  (*API_SHLWAPI_DLL_PathIsDirectoryA)(local_108);
  local_10c = FUN__text__0056ce80();
  uStack_14 = 0x42a9b5;
  FUN__text__0056ce80();
  return;
}

