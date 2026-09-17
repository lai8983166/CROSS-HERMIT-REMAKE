
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text1__0084daa2(uint param_1)

{
  HANDLE hFile;
  BOOL BVar1;
  DWORD DVar2;
  
  DVar2 = _DAT_00875650;
  if ((param_1 < DAT_00876c60) &&
     ((*(byte *)((&DAT_00876b60)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 8) & 1) != 0)) {
    hFile = (HANDLE)FUN__text1__0084d482(param_1);
    BVar1 = FlushFileBuffers(hFile);
    if (BVar1 == 0) {
      DVar2 = GetLastError();
    }
    else {
      DVar2 = 0;
    }
    if (DVar2 == 0) {
      return 0;
    }
  }
  _DAT_00875650 = DVar2;
  _DAT_0087564c = 9;
  return 0xffffffff;
}

