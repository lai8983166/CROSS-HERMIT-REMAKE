
undefined4 FUN__text1__00837283(HANDLE param_1)

{
  char cVar1;
  HANDLE hThread;
  DWORD DVar2;
  uint uVar3;
  HMODULE hInstance;
  BOOL BVar4;
  int iVar5;
  LPVOID lpParam;
  tagMSG local_178;
  uint local_15c;
  uint local_158;
  int local_154;
  char local_150 [256];
  WNDCLASSA local_50;
  HANDLE local_28;
  char *local_24;
  HWND local_20;
  undefined1 *local_1c;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_00872e10;
  puStack_10 = &LAB__text1__00849320;
  local_14 = ExceptionList;
  local_1c = &stack0xfffffe50;
  local_28 = param_1;
  iVar5 = 2;
  ExceptionList = &local_14;
  hThread = GetCurrentThread();
  SetThreadPriority(hThread,iVar5);
  do {
    cVar1 = FUN__text1__00837667(local_28);
    if (cVar1 == '\0') goto LAB__text1__008372f9;
    DVar2 = WaitForInputIdle(local_28,500);
  } while (DVar2 == 0x102);
  Sleep(0xfa);
LAB__text1__008372f9:
  cVar1 = FUN__text1__00837667(local_28);
  if (cVar1 != '\0') {
    WaitForInputIdle(local_28,30000);
    Sleep(500);
    uVar3 = FUN__text1__008494b6(0);
    DVar2 = GetTickCount();
    iVar5 = (int)(uVar3 ^ DVar2) % 10000;
    local_158 = ((((uint)(iVar5 * 0xc45 + ((int)(uVar3 ^ DVar2) / 10000) * 0x16bd) % 10000) * 10000
                 + iVar5 * 0x16bd) % 100000000 + 1) % 100000000;
    local_24 = local_150;
    local_154 = ((local_158 / 10000) * 10) / 10000 + 4;
    while (local_154 != 0) {
      local_158 = (((((local_158 % 10000) * 0xc45 + (local_158 / 10000) * 0x16bd) % 10000) * 10000 +
                   (local_158 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
      local_15c = ((local_158 / 10000) * 0x34) / 10000;
      *local_24 = (-(local_15c < 0x1a) & 0x20U) + 0x41 + (char)((ulonglong)local_15c % 0x1a);
      local_24 = local_24 + 1;
      local_154 = local_154 + -1;
    }
    *local_24 = '\0';
    local_154 = local_154 + -1;
    _memset(&local_50,0,0x28);
    local_50.lpfnWndProc = FUN__text1__0083768a;
    local_50.hInstance = GetModuleHandleA((LPCSTR)0x0);
    local_50.lpszClassName = local_150;
    RegisterClassA(&local_50);
    lpParam = (LPVOID)0x0;
    hInstance = GetModuleHandleA((LPCSTR)0x0);
    local_20 = CreateWindowExA(0,local_150,(LPCSTR)0x0,0xcf0000,-0x80000000,-0x80000000,-0x80000000,
                               -0x80000000,(HWND)0x0,(HMENU)0x0,hInstance,lpParam);
    SetTimer(local_20,1,10000,(TIMERPROC)0x0);
    local_8 = 0;
    while ((cVar1 = FUN__text1__00837667(local_28), cVar1 != '\0' &&
           (BVar4 = GetMessageA(&local_178,(HWND)0x0,0,0), 0 < BVar4))) {
      TranslateMessage(&local_178);
      DispatchMessageA(&local_178);
    }
  }
  ExceptionList = local_14;
  return 0;
}

