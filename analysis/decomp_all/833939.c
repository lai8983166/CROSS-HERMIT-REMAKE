
HWND FUN__text1__00833939(void)

{
  char cVar1;
  HMODULE pHVar2;
  HWND pHVar3;
  LPVOID pvVar4;
  WNDCLASSA local_60;
  wchar_t *local_34;
  WNDCLASSW local_30;
  
  cVar1 = FUN__text1__0083309d();
  if (cVar1 == '\0') {
    local_60.style = 0xb;
    local_60.lpfnWndProc = FUN__text1__00833aa4;
    local_60.cbClsExtra = 0;
    local_60.cbWndExtra = 0;
    local_60.hInstance = GetModuleHandleA((LPCSTR)0x0);
    local_60.hIcon = (HICON)0x0;
    local_60.hCursor = LoadCursorA((HINSTANCE)0x0,(LPCSTR)0x7f00);
    local_60.hbrBackground = (HBRUSH)0x6;
    local_60.lpszMenuName = (LPCSTR)0x0;
    local_60.lpszClassName = "SwPDDE";
    RegisterClassA(&local_60);
    pvVar4 = (LPVOID)0x0;
    pHVar2 = GetModuleHandleA((LPCSTR)0x0);
    pHVar3 = CreateWindowExA(0x40300,"SwPDDE","DDE Processing",0x2cf0000,-0x80000000,-0x80000000,
                             -0x80000000,-0x80000000,(HWND)0x0,(HMENU)0x0,pHVar2,pvVar4);
  }
  else {
    local_34 = L"SwPDDE";
    local_30.style = 0xb;
    local_30.lpfnWndProc = FUN__text1__00833aa4;
    local_30.cbClsExtra = 0;
    local_30.cbWndExtra = 0;
    local_30.hInstance = GetModuleHandleA((LPCSTR)0x0);
    local_30.hIcon = (HICON)0x0;
    local_30.hCursor = LoadCursorA((HINSTANCE)0x0,(LPCSTR)0x7f00);
    local_30.hbrBackground = (HBRUSH)0x6;
    local_30.lpszMenuName = (LPCWSTR)0x0;
    local_30.lpszClassName = local_34;
    RegisterClassW(&local_30);
    pvVar4 = (LPVOID)0x0;
    pHVar2 = GetModuleHandleA((LPCSTR)0x0);
    pHVar3 = CreateWindowExW(0x40300,local_34,L"DDE Processing",0x2cf0000,-0x80000000,-0x80000000,
                             -0x80000000,-0x80000000,(HWND)0x0,(HMENU)0x0,pHVar2,pvVar4);
  }
  return pHVar3;
}

