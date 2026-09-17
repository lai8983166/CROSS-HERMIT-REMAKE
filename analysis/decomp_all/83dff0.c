
void FUN__text1__0083dff0(char param_1)

{
  HMODULE hInstance;
  DWORD DVar1;
  LPVOID lpParam;
  
  if (DAT_00875438 == '\0') {
    FUN__text1__0083e0c4();
  }
  if ((((param_1 == '\0') || (DAT_00875640 != (HWND)0x0)) || (DAT_00875434 != '\0')) ||
     (DAT_00875435 != '\0')) {
    if ((param_1 == '\0') && (DAT_00875640 != (HWND)0x0)) {
      DestroyWindow(DAT_00875640);
      DAT_00875640 = (HWND)0x0;
    }
  }
  else {
    lpParam = (LPVOID)0x0;
    hInstance = GetModuleHandleA((LPCSTR)0x0);
    DAT_00875640 = CreateWindowExA(0x40000,"LISTBOX","",0x10f45100,-0x80000000,-0x80000000,
                                   -0x80000000,-0x80000000,(HWND)0x0,(HMENU)0x0,hInstance,lpParam);
    if (DAT_00875640 == (HWND)0x0) {
      DVar1 = GetLastError();
      FUN__text1__0083e144("RAID error %u creating listwindow, reverting to older format.",DVar1);
    }
  }
  return;
}

