
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

DWORD FUN__text1__0084c0b7(uint param_1,LONG param_2,DWORD param_3)

{
  byte *pbVar1;
  HANDLE hFile;
  DWORD DVar2;
  DWORD DVar3;
  int iVar4;
  
  if (param_1 < DAT_00876c60) {
    iVar4 = (param_1 & 0x1f) * 8;
    if ((*(byte *)((&DAT_00876b60)[(int)param_1 >> 5] + 4 + iVar4) & 1) != 0) {
      hFile = (HANDLE)FUN__text1__0084d482(param_1);
      if (hFile == (HANDLE)0xffffffff) {
        _DAT_0087564c = 9;
        return 0xffffffff;
      }
      DVar2 = SetFilePointer(hFile,param_2,(PLONG)0x0,param_3);
      if (DVar2 == 0xffffffff) {
        DVar3 = GetLastError();
      }
      else {
        DVar3 = 0;
      }
      if (DVar3 != 0) {
        FUN__text1__0084d3a1(DVar3);
        return 0xffffffff;
      }
      pbVar1 = (byte *)((&DAT_00876b60)[(int)param_1 >> 5] + 4 + iVar4);
      *pbVar1 = *pbVar1 & 0xfd;
      return DVar2;
    }
  }
  _DAT_00875650 = 0;
  _DAT_0087564c = 9;
  return 0xffffffff;
}

