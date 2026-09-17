
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text1__008495e3(void)

{
  DWORD DVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  HMODULE pHVar5;
  undefined4 uVar6;
  _STARTUPINFOA local_60;
  undefined1 *local_1c;
  undefined4 *local_18;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_00873f88;
  puStack_10 = &LAB__text1__00849320;
  pvStack_14 = ExceptionList;
  local_1c = &stack0xffffff88;
  ExceptionList = &pvStack_14;
  DVar1 = GetVersion();
  _DAT_00875664 = DVar1 >> 8 & 0xff;
  _DAT_00875660 = DVar1 & 0xff;
  _DAT_0087565c = _DAT_00875660 * 0x100 + _DAT_00875664;
  _DAT_00875658 = DVar1 >> 0x10;
  iVar2 = FUN__text1__0084acba(0);
  if (iVar2 == 0) {
    FUN__text1__008496fe(0x1c);
  }
  local_8 = 0;
  FUN__text1__0084a99a();
  DAT_00876c64 = GetCommandLineA();
  DAT_008756b8 = FUN__text1__0084a868();
  FUN__text1__0084a61b();
  FUN__text1__0084a562();
  FUN__text1__008490a8();
  local_60.dwFlags = 0;
  GetStartupInfoA(&local_60);
  uVar3 = FUN__text1__0084a50a();
  if ((local_60.dwFlags & 1) == 0) {
    uVar4 = 10;
  }
  else {
    uVar4 = (uint)local_60.wShowWindow;
  }
  uVar6 = 0;
  pHVar5 = GetModuleHandleA((LPCSTR)0x0);
  uVar3 = FUN__text1__00835d60(pHVar5,uVar6,uVar3,uVar4);
  FUN__text1__008490d5(uVar3);
  FUN__text1__0084a386(*(undefined4 *)*local_18,local_18);
  return;
}

