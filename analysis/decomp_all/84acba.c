
undefined4 FUN__text1__0084acba(int param_1)

{
  int iVar1;
  
  DAT_00876b40 = HeapCreate((uint)(param_1 == 0),0x1000,0);
  if (DAT_00876b40 != (HANDLE)0x0) {
    DAT_00876b44 = FUN__text1__0084ab72();
    if (DAT_00876b44 == 3) {
      iVar1 = FUN__text1__0084aea3(0x3f8);
    }
    else {
      if (DAT_00876b44 != 2) {
        return 1;
      }
      iVar1 = FUN__text1__0084b9ea();
    }
    if (iVar1 != 0) {
      return 1;
    }
    HeapDestroy(DAT_00876b40);
  }
  return 0;
}

