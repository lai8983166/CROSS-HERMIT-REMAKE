
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text1__0084d408(uint param_1)

{
  int *piVar1;
  int iVar2;
  DWORD nStdHandle;
  
  if (param_1 < DAT_00876c60) {
    iVar2 = (param_1 & 0x1f) * 8;
    piVar1 = (int *)((&DAT_00876b60)[(int)param_1 >> 5] + iVar2);
    if (((*(byte *)(piVar1 + 1) & 1) != 0) && (*piVar1 != -1)) {
      if (DAT_00870254 == 1) {
        if (param_1 == 0) {
          nStdHandle = 0xfffffff6;
        }
        else if (param_1 == 1) {
          nStdHandle = 0xfffffff5;
        }
        else {
          if (param_1 != 2) goto LAB__text1__0084d461;
          nStdHandle = 0xfffffff4;
        }
        SetStdHandle(nStdHandle,(HANDLE)0x0);
      }
LAB__text1__0084d461:
      *(undefined4 *)((&DAT_00876b60)[(int)param_1 >> 5] + iVar2) = 0xffffffff;
      return 0;
    }
  }
  _DAT_00875650 = 0;
  _DAT_0087564c = 9;
  return 0xffffffff;
}

