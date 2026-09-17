
void FUN__text__00426bc0(undefined1 *param_1,int param_2,int param_3)

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
  if (local_10 == 0) {
    *param_1 = 0;
  }
  else {
    local_14 = local_10 + 2;
    if (param_3 < local_10) {
      local_20 = (void *)FUN__text__00428a40(local_14 * 2);
      local_c = local_20;
      if ((local_20 == (void *)0x0) &&
         (iVar2 = FUN__text__00424f80(&DAT_00594bdc,"e:\\crosshermit\\game\\src\\system\\sysime.cpp"
                                      ,DAT_005ff694 + 0x11,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      _memset(local_c,0,local_14 << 1);
      (*API_KERNEL32_DLL_MultiByteToWideChar)(0,0,param_1,0xffffffff,local_c,local_14);
      local_1c = FUN__text__0056ce80();
      if ((local_1c == 0) &&
         (iVar2 = FUN__text__00424f80(&DAT_00594c9c,"e:\\crosshermit\\game\\src\\system\\sysime.cpp"
                                      ,DAT_005ff694 + 0x15,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      *(undefined2 *)((int)local_c + param_3 * 2) = 0;
      (*API_KERNEL32_DLL_WideCharToMultiByte)(0,0,local_c,0xffffffff,param_1,param_2,0,0);
      local_18 = FUN__text__0056ce80();
      if ((local_18 == 0) &&
         (iVar2 = FUN__text__00424f80(&DAT_00594c50,"e:\\crosshermit\\game\\src\\system\\sysime.cpp"
                                      ,DAT_005ff694 + 0x23,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if ((param_2 < local_18) &&
         (iVar2 = FUN__text__00424f80(&DAT_00594be4,"e:\\crosshermit\\game\\src\\system\\sysime.cpp"
                                      ,DAT_005ff694 + 0x24,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_24 = local_c;
      FUN__text__00428ad0(local_c);
    }
  }
  local_c = (void *)0x426d81;
  FUN__text__0056ce80();
  return;
}

