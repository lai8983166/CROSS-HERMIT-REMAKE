
HBITMAP FUN__text1__00836208(int param_1,LONG *param_2,LONG *param_3)

{
  int iVar1;
  byte bVar2;
  LOGPALETTE *plpal;
  RGBQUAD *local_70;
  uint local_6c;
  RGBQUAD *local_68;
  uint local_64;
  BITMAPINFOHEADER local_5c;
  HDC local_34;
  BITMAPINFO *local_30;
  void *local_2c;
  HPALETTE local_28;
  uint local_24;
  short local_20;
  undefined2 uStack_1e;
  undefined2 uStack_1c;
  int local_16;
  HBITMAP local_10;
  int local_c;
  void *local_8;
  
  local_8 = (void *)param_1;
  FUN__text1__00848490(&local_20,param_1,0xe);
  local_8 = (void *)((int)local_8 + 0xe);
  if (local_20 == 0x4d42) {
    FUN__text1__00848490(&local_5c,local_8,0x28);
    local_8 = (void *)((int)local_8 + 0x28);
    bVar2 = (byte)local_5c.biBitCount;
    if (local_5c.biClrUsed == 0) {
      local_5c.biClrUsed = 1 << (bVar2 & 0x1f);
    }
    if (local_5c.biClrImportant == 0) {
      local_5c.biClrImportant = 1 << (bVar2 & 0x1f);
    }
    if (local_5c.biBitCount < 9) {
      iVar1 = (1 << (bVar2 & 0x1f)) * 4;
    }
    else {
      iVar1 = local_5c.biClrUsed * 2;
    }
    local_24 = iVar1 + 0x28;
    local_30 = operator_new(local_24);
    (local_30->bmiHeader).biSize = 0x28;
    (local_30->bmiHeader).biWidth = local_5c.biWidth;
    (local_30->bmiHeader).biHeight = local_5c.biHeight;
    (local_30->bmiHeader).biPlanes = local_5c.biPlanes;
    (local_30->bmiHeader).biBitCount = local_5c.biBitCount;
    (local_30->bmiHeader).biCompression =
         CONCAT22(local_5c.biCompression._2_2_,(undefined2)local_5c.biCompression);
    (local_30->bmiHeader).biSizeImage = local_5c.biSizeImage;
    (local_30->bmiHeader).biXPelsPerMeter = local_5c.biXPelsPerMeter;
    (local_30->bmiHeader).biYPelsPerMeter = local_5c.biYPelsPerMeter;
    (local_30->bmiHeader).biClrUsed = local_5c.biClrUsed;
    (local_30->bmiHeader).biClrImportant = local_5c.biClrImportant;
    if (local_5c.biBitCount < 9) {
      local_c = local_5c.biClrUsed * (((local_30->bmiHeader).biSize == 0x28) + 3);
      FUN__text1__00848490(local_30->bmiColors,local_8,local_c);
      local_8 = (void *)((int)local_8 + local_c);
      plpal = operator_new(local_5c.biClrUsed * 0x10 + 0x20);
      plpal->palVersion = 0x300;
      plpal->palNumEntries = (WORD)local_5c.biClrUsed;
      if ((local_30->bmiHeader).biSize == 0x28) {
        local_68 = local_30->bmiColors;
        for (local_64 = 0; local_64 < plpal->palNumEntries; local_64 = local_64 + 1) {
          plpal->palPalEntry[local_64].peRed = local_68->rgbRed;
          plpal->palPalEntry[local_64].peGreen = local_68->rgbGreen;
          plpal->palPalEntry[local_64].peBlue = local_68->rgbBlue;
          plpal->palPalEntry[local_64].peFlags = '\0';
          local_68 = local_68 + 1;
        }
      }
      else {
        local_70 = local_30->bmiColors;
        for (local_6c = 0; local_6c < plpal->palNumEntries; local_6c = local_6c + 1) {
          plpal->palPalEntry[local_6c].peRed = local_70->rgbRed;
          plpal->palPalEntry[local_6c].peGreen = local_70->rgbGreen;
          plpal->palPalEntry[local_6c].peBlue = local_70->rgbBlue;
          plpal->palPalEntry[local_6c].peFlags = '\0';
          local_70 = (RGBQUAD *)&local_70->rgbReserved;
        }
      }
      DAT_00875208 = CreatePalette(plpal);
      FUN__text1__00848476(plpal);
    }
    local_c = CONCAT22(uStack_1c,uStack_1e) - local_16;
    local_2c = local_8;
    local_8 = (void *)((int)local_8 + local_c);
    local_34 = CreateDCA("DISPLAY",(LPCSTR)0x0,(LPCSTR)0x0,(DEVMODEA *)0x0);
    local_28 = (HPALETTE)0x0;
    if (DAT_00875208 != (HPALETTE)0x0) {
      local_28 = SelectPalette(local_34,DAT_00875208,0);
      RealizePalette(local_34);
    }
    local_10 = CreateDIBitmap(local_34,&local_5c,4,local_2c,local_30,0);
    if (local_28 != (HPALETTE)0x0) {
      SelectPalette(local_34,local_28,0);
    }
    DeleteDC(local_34);
    FUN__text1__00848476(local_30);
    if (param_2 != (LONG *)0x0) {
      *param_2 = local_5c.biWidth;
    }
    if (param_3 != (LONG *)0x0) {
      *param_3 = local_5c.biHeight;
    }
  }
  else {
    local_10 = (HBITMAP)0x0;
  }
  return local_10;
}

