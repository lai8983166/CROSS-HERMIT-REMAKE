
void FUN__text__00424fc0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_150 [16];
  uint local_110;
  undefined1 local_10c [252];
  undefined4 uStack_10;
  int local_8;
  
  puVar2 = local_150;
  for (iVar1 = 0x53; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_GetCurrentDirectoryA)(0x104,local_10c);
  local_110 = FUN__text__0056ce80();
  if (local_110 < 0x105) {
    FUN__text__004297a0(local_10c);
    (*API_KERNEL32_DLL_lstrcatA)(local_10c,"DebugAssert.log");
    FUN__text__0056ce80();
    local_8 = FUN__text__0056e7c0(local_10c,&DAT_00594ad0);
    if (local_8 != 0) {
      FUN__text__0056e5f0(local_8,&DAT_00592a18,param_1);
      FUN__text__0056e4a0(local_8);
    }
  }
  uStack_10 = 0x425085;
  FUN__text__0056ce80();
  return;
}

