
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text1__0084dba6(uint param_1)

{
  int iVar1;
  int iVar2;
  HANDLE hObject;
  BOOL BVar3;
  DWORD DVar4;
  int iVar5;
  
  if (DAT_00876c60 <= param_1) {
    _DAT_00875650 = 0;
    _DAT_0087564c = 9;
    return 0xffffffff;
  }
  iVar5 = (param_1 & 0x1f) * 8;
  if ((*(byte *)((&DAT_00876b60)[(int)param_1 >> 5] + 4 + iVar5) & 1) == 0) {
    _DAT_0087564c = 9;
    _DAT_00875650 = 0;
    return 0xffffffff;
  }
  iVar1 = FUN__text1__0084d482(param_1);
  if (iVar1 != -1) {
    if ((param_1 == 1) || (param_1 == 2)) {
      iVar1 = FUN__text1__0084d482(2);
      iVar2 = FUN__text1__0084d482(1);
      if (iVar2 == iVar1) goto LAB__text1__0084dc1f;
    }
    hObject = (HANDLE)FUN__text1__0084d482(param_1);
    BVar3 = CloseHandle(hObject);
    if (BVar3 == 0) {
      DVar4 = GetLastError();
      goto LAB__text1__0084dc21;
    }
  }
LAB__text1__0084dc1f:
  DVar4 = 0;
LAB__text1__0084dc21:
  FUN__text1__0084d408(param_1);
  *(undefined1 *)((&DAT_00876b60)[(int)param_1 >> 5] + 4 + iVar5) = 0;
  if (DVar4 == 0) {
    return 0;
  }
  FUN__text1__0084d3a1(DVar4);
  return 0xffffffff;
}

