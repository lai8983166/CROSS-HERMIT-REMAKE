
void FUN__text__004266e0(undefined4 param_1,undefined4 param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [13];
  undefined4 uStack_2c;
  undefined2 local_20 [2];
  int local_1c;
  undefined1 local_18 [8];
  int local_10;
  undefined4 local_c;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = 0;
  local_20[0] = DAT_005926c4;
  local_c = FUN__text__00414440();
  (*API_GDI32_DLL_SelectObject)(local_c,param_2);
  local_10 = FUN__text__0056ce80();
  if (local_10 == 0) {
    iVar3 = FUN__text__00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                DAT_005ff68c + 10,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_KERNEL32_DLL_lstrlenA)(local_20,local_18);
  uVar2 = FUN__text__0056ce80();
  (*API_GDI32_DLL_GetTextExtentPoint32A)(local_c,local_20,uVar2);
  local_1c = FUN__text__0056ce80();
  if (local_1c == 0) {
    iVar3 = FUN__text__00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                DAT_005ff68c + 0xd,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_GDI32_DLL_SelectObject)(local_c,local_10);
  local_10 = FUN__text__0056ce80();
  if (local_10 == 0) {
    iVar3 = FUN__text__00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                DAT_005ff68c + 0x10,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  uStack_2c = 0x42680c;
  FUN__text__0056ce80();
  return;
}

