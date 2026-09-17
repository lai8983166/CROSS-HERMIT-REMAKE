
int FUN__text1__0084d318(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  HMODULE hModule;
  int iVar1;
  
  iVar1 = 0;
  if (DAT_008758a8 == (FARPROC)0x0) {
    hModule = LoadLibraryA("user32.dll");
    if (hModule != (HMODULE)0x0) {
      DAT_008758a8 = GetProcAddress(hModule,"MessageBoxA");
      if (DAT_008758a8 != (FARPROC)0x0) {
        DAT_008758ac = GetProcAddress(hModule,"GetActiveWindow");
        DAT_008758b0 = GetProcAddress(hModule,"GetLastActivePopup");
        goto LAB__text1__0084d367;
      }
    }
    iVar1 = 0;
  }
  else {
LAB__text1__0084d367:
    if (DAT_008758ac != (FARPROC)0x0) {
      iVar1 = (*DAT_008758ac)();
      if ((iVar1 != 0) && (DAT_008758b0 != (FARPROC)0x0)) {
        iVar1 = (*DAT_008758b0)(iVar1);
      }
    }
    iVar1 = (*DAT_008758a8)(iVar1,param_1,param_2,param_3);
  }
  return iVar1;
}

