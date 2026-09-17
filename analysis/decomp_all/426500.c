
void FUN__text__00426500(undefined4 param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [12];
  undefined4 uStack_20;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  local_c = FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrlenA)(param_2);
  local_10 = FUN__text__0056ce80();
  if (0x3e < local_c + local_10) {
    iVar2 = FUN__text__00424f80("(len0+len1) < (32*2-1)",
                                "e:\\crosshermit\\game\\src\\system\\sysime.cpp",DAT_005ff688 + 5,0)
    ;
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0x6fc,param_1);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcatA)(local_8 + 0x6fc,param_2);
  FUN__text__0056ce80();
  FUN__text__00426d90(local_8 + 0x63c,local_8 + 0x6fc,0x40);
  uStack_20 = 0x4265e4;
  FUN__text__0056ce80();
  return;
}

