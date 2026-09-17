
void FUN__text__0042a030(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_150 [16];
  int local_110;
  undefined4 local_10c;
  undefined1 local_108 [244];
  undefined4 uStack_14;
  
  puVar2 = local_150;
  for (iVar1 = 0x53; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_lstrcpyA)(local_108,param_1);
  FUN__text__0056ce80();
  FUN__text__004297e0(local_108);
  (*API_SHLWAPI_DLL_PathStripToRootA)(local_108);
  local_110 = FUN__text__0056ce80();
  if (local_110 == 1) {
    (*API_KERNEL32_DLL_lstrlenA)(local_108);
    local_10c = FUN__text__0056ce80();
  }
  uStack_14 = 0x42a0f9;
  FUN__text__0056ce80();
  return;
}

