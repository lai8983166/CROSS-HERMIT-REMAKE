
LRESULT FUN__text1__008368f4(HWND param_1,uint param_2,WPARAM param_3,LPARAM param_4)

{
  ushort uVar1;
  HDC hdc;
  DWORD DVar2;
  LRESULT LVar3;
  tagPAINTSTRUCT local_54;
  HDC local_14;
  HGDIOBJ local_10;
  HPALETTE local_c;
  int local_8;
  
  if (param_2 < 0x203) {
    if (param_2 == 0x202) {
LAB__text1__00836a31:
      if (DAT_0087520c != '\0') {
        FUN__text1__00836190();
      }
      return 0;
    }
    if (param_2 == 2) {
      if (DAT_00875204 != (HGDIOBJ)0x0) {
        DeleteObject(DAT_00875204);
        DAT_00875204 = (HGDIOBJ)0x0;
      }
      if (DAT_00875208 != (HPALETTE)0x0) {
        DeleteObject(DAT_00875208);
        DAT_00875208 = (HPALETTE)0x0;
      }
      return 0;
    }
    if (param_2 == 0xf) {
      local_14 = BeginPaint(param_1,&local_54);
      hdc = CreateCompatibleDC(local_14);
      local_10 = SelectObject(hdc,DAT_00875204);
      local_c = (HPALETTE)0x0;
      if (DAT_00875208 != (HPALETTE)0x0) {
        local_c = SelectPalette(local_14,DAT_00875208,0);
        RealizePalette(local_14);
      }
      BitBlt(local_14,0,0,DAT_008751f8,DAT_008751f4,hdc,0,0,0xcc0020);
      if (local_c != (HPALETTE)0x0) {
        SelectPalette(local_14,local_c,0);
      }
      SelectObject(hdc,local_10);
      DeleteDC(hdc);
      EndPaint(param_1,&local_54);
      return 0;
    }
    if (param_2 == 0x113) {
      if (param_3 == 2) {
        for (local_8 = 0; local_8 < 0x100; local_8 = local_8 + 1) {
          uVar1 = GetAsyncKeyState(local_8);
          if ((uVar1 & 1) != 0) {
            FUN__text1__00836190();
            return 0;
          }
        }
      }
      else if ((param_3 == 1) && (DVar2 = GetTickCount(), DAT_00875214 <= DVar2)) {
        KillTimer(param_1,1);
        SendMessageA(param_1,0x40a,0,0);
      }
      return 0;
    }
  }
  else {
    if ((param_2 == 0x205) || (param_2 == 0x208)) goto LAB__text1__00836a31;
    if (param_2 == 0x40a) {
      DestroyWindow(param_1);
      return 0;
    }
  }
  LVar3 = DefWindowProcA(param_1,param_2,param_3,param_4);
  return LVar3;
}

