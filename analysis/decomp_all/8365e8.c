
undefined * FUN__text1__008365e8(int param_1,int param_2,char param_3,char param_4,char param_5)

{
  DWORD DVar1;
  HANDLE hObject;
  int iVar2;
  undefined *puVar3;
  LPCSTR local_14c;
  LPCSTR local_148;
  int local_144;
  WNDCLASSA local_140;
  uint local_118;
  int local_114;
  int local_110;
  char *local_10c;
  CHAR local_108 [256];
  char *local_8;
  
  local_10c = "ArBase Bitmap Window";
  local_8 = "ArBase Test Bitmap Window";
  DAT_0087520c = param_4;
  DAT_0087520d = param_3;
  DAT_008751f8 = param_1;
  DAT_008751f4 = param_2;
  if ((param_5 == '\0') || (param_4 != '\0')) {
    DAT_00875210 = GetCurrentThreadId();
    if (DAT_00875218 == '\0') {
      local_140.style = 0;
      local_140.lpfnWndProc = FUN__text1__008368f4;
      local_140.cbClsExtra = 0;
      local_140.cbWndExtra = 0;
      local_140.hInstance = (HINSTANCE)PTR_IMAGE_DOS_HEADER_008751e8;
      local_140.hIcon = (HICON)0x0;
      local_140.hCursor =
           LoadCursorA((HINSTANCE)0x0,
                       (LPCSTR)((-(uint)(DAT_0087520c != '\0') & 0xfffffffe) + 0x7f02));
      local_140.hbrBackground = (HBRUSH)0x0;
      local_140.lpszMenuName = (LPCSTR)0x0;
      if (param_4 == '\0') {
        local_148 = local_10c;
      }
      else {
        local_148 = local_8;
      }
      local_140.lpszClassName = local_148;
      RegisterClassA(&local_140);
      DAT_00875218 = '\x01';
    }
    if (param_4 != '\0') {
      for (local_144 = 0; local_144 < 0x100; local_144 = local_144 + 1) {
        GetAsyncKeyState(local_144);
      }
    }
    iVar2 = GetSystemMetrics(0);
    local_114 = (iVar2 - DAT_008751f8) / 2;
    iVar2 = GetSystemMetrics(1);
    local_110 = (iVar2 - DAT_008751f4) / 2;
    if (param_4 == '\0') {
      local_14c = local_10c;
    }
    else {
      local_14c = local_8;
    }
    PTR_DAT_00875200 =
         (undefined *)
         CreateWindowExA((-(uint)(param_3 != '\0') & 0xffffff88) + 0x80,local_14c,(LPCSTR)0x0,
                         (-(uint)(DAT_0087520c != '\0') & 0xf8000000) + 0x8000000 | 0x80000000,
                         local_114,local_110,DAT_008751f8,DAT_008751f4,(HWND)0x0,(HMENU)0x0,
                         (HINSTANCE)PTR_IMAGE_DOS_HEADER_008751e8,(LPVOID)0x0);
    ShowWindow((HWND)PTR_DAT_00875200,4);
    UpdateWindow((HWND)PTR_DAT_00875200);
    if (param_4 != '\0') {
      SetTimer((HWND)PTR_DAT_00875200,2,100,(TIMERPROC)0x0);
    }
    FUN__text1__008491aa(local_108,&DAT_0086e698,PTR_DAT_00875200);
    SetEnvironmentVariableA("LOADINGWINDOW",local_108);
    DAT_00875219 = '\0';
    puVar3 = PTR_DAT_00875200;
  }
  else {
    DAT_00875219 = '\x01';
    DVar1 = GetTickCount();
    local_118 = DVar1 + 0xfa;
    hObject = CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,FUN__text1__00836b30,(LPVOID)0x0,0,
                           &DAT_00875210);
    CloseHandle(hObject);
    while (DAT_00875219 != '\0') {
      DVar1 = GetTickCount();
      if (local_118 <= DVar1) break;
      Sleep(1);
    }
    puVar3 = (undefined *)0x1;
  }
  return puVar3;
}

