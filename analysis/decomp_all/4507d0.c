
void FUN__text__004507d0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [13];
  undefined4 uStack_18;
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__00428d60("SOFTWARE\\Enterbrain\\Cross Hermit");
  if (local_c == 0) {
    local_c = FUN__text__00428ff0("InstallPath",local_8 + 0x8e8,0x104);
    if (local_c != 0) {
LAB__text__00450a07:
      FUN__text__00428e00();
      (*DAT_005923d8)(PTR_DAT_007a0bb4,&DAT_00598760,"Cross Hermit",0x10);
      local_c = FUN__text__0056ce80();
      goto LAB__text__00450a49;
    }
    FUN__text__00429580(local_8 + 0x8e8);
    iVar1 = FUN__text__0042a930(local_8 + 0x8e8);
    if (iVar1 == 1) {
      (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0xbf4,local_8 + 0x8e8);
      FUN__text__0056ce80();
      (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0xcf8,local_8 + 0x8e8);
      FUN__text__0056ce80();
      (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0xdfc,local_8 + 0x8e8);
      FUN__text__0056ce80();
      (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0x1004,local_8 + 0x8e8);
      FUN__text__0056ce80();
      (*API_KERNEL32_DLL_lstrcatA)(local_8 + 0x1004,"SaveData\\");
      FUN__text__0056ce80();
      local_c = FUN__text__00428ff0("VoicePath",local_8 + 0x8e8,0x104);
      if (local_c != 0) goto LAB__text__00450a07;
      FUN__text__00429580(local_8 + 0x8e8);
      iVar1 = FUN__text__0042a930(local_8 + 0x8e8);
      if (iVar1 == 1) {
        (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0xf00,local_8 + 0x8e8);
        FUN__text__0056ce80();
        FUN__text__00428e00();
        goto LAB__text__00450a49;
      }
    }
    (*DAT_005923d8)(PTR_DAT_007a0bb4,&DAT_00598798,"Cross Hermit",0x10);
    local_c = FUN__text__0056ce80();
  }
  else {
    (*DAT_005923d8)(PTR_DAT_007a0bb4,&DAT_005987d0,"Cross Hermit",0x10);
    local_c = FUN__text__0056ce80();
  }
  FUN__text__00428e00();
LAB__text__00450a49:
  uStack_18 = 0x450a56;
  FUN__text__0056ce80();
  return;
}

