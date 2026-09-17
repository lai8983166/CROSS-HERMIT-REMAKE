
undefined4 FUN__text1__00836b30(void)

{
  DWORD DVar1;
  BOOL BVar2;
  tagMSG local_24;
  HWND local_8;
  
  local_8 = (HWND)FUN__text1__008365e8(DAT_008751f8,DAT_008751f4,DAT_0087520d,DAT_0087520c,0);
  if (local_8 != (HWND)0x0) {
    if (DAT_008751fc != 0) {
      DVar1 = GetTickCount();
      DAT_00875214 = DVar1 + DAT_008751fc * 1000;
    }
    SetTimer(local_8,1,0xfa,(TIMERPROC)0x0);
    while (BVar2 = IsWindow(local_8), BVar2 != 0) {
      BVar2 = PeekMessageA(&local_24,local_8,0,0,3);
      if (BVar2 == 0) {
        Sleep(1);
      }
      else {
        if (local_24.message == 0x12) {
          return 0;
        }
        TranslateMessage(&local_24);
        DispatchMessageA(&local_24);
      }
    }
  }
  return 0;
}

