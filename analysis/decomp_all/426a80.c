
void FUN__text__00426a80(undefined4 param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  void *local_24;
  void *local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  void *local_c;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  local_10 = FUN__text__0056ce80();
  if (local_10 != 0) {
    local_14 = local_10 + 1;
    local_20 = (void *)FUN__text__00428a40(local_14 * 2);
    local_c = local_20;
    if ((local_20 == (void *)0x0) &&
       (iVar2 = FUN__text__00424f80(&DAT_00594bdc,"e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                    DAT_005ff690 + 10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    _memset(local_c,0,local_14 << 1);
    (*API_KERNEL32_DLL_MultiByteToWideChar)(0,0,param_1,0xffffffff,local_c,local_14);
    local_18 = FUN__text__0056ce80();
    if ((local_18 == 0) &&
       (iVar2 = FUN__text__00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                    DAT_005ff690 + 0xe,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    for (local_1c = 0; *(short *)((int)local_c + local_1c * 2) != 0; local_1c = local_1c + 1) {
    }
    local_24 = local_c;
    FUN__text__00428ad0(local_c);
  }
  local_c = (void *)0x426bb4;
  FUN__text__0056ce80();
  return;
}

