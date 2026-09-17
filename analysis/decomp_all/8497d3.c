
void FUN__text1__008497d3(LPVOID param_1)

{
  LPVOID lpMem;
  int iVar1;
  undefined4 local_8;
  
  lpMem = param_1;
  if (param_1 != (LPVOID)0x0) {
    if (DAT_00876b44 == 3) {
      iVar1 = FUN__text1__0084aeeb(param_1);
      if (iVar1 != 0) {
        FUN__text1__0084af16(iVar1);
        return;
      }
    }
    else if ((DAT_00876b44 == 2) &&
            (iVar1 = FUN__text1__0084bc46(param_1,&local_8,&param_1), iVar1 != 0)) {
      FUN__text1__0084bc9d(local_8,param_1,iVar1);
      return;
    }
    HeapFree(DAT_00876b40,0,lpMem);
  }
  return;
}

