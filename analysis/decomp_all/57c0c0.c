
void FUN__text__0057c0c0(void)

{
  int iVar1;
  uint local_520;
  undefined1 local_51c [256];
  undefined1 local_41c [256];
  undefined1 local_31c [6];
  byte local_316 [14];
  undefined1 local_308 [256];
  ushort local_208 [256];
  byte *local_8;
  
  iVar1 = (*API_KERNEL32_DLL_GetCPInfo)(DAT_0080a904,local_31c);
  if (iVar1 == 1) {
    for (local_520 = 0; local_520 < 0x100; local_520 = local_520 + 1) {
      local_308[local_520] = (undefined1)local_520;
    }
    local_308[0] = 0x20;
    for (local_8 = local_316; *local_8 != 0; local_8 = local_8 + 2) {
      for (local_520 = (uint)*local_8; local_520 <= local_8[1]; local_520 = local_520 + 1) {
        local_308[local_520] = 0x20;
      }
    }
    FUN__text__00587230(1,local_308,0x100,local_208,DAT_0080a904,DAT_0080ab24,0);
    FUN__text__005873f0(DAT_0080ab24,0x100,local_308,0x100,local_41c,0x100,DAT_0080a904,0);
    FUN__text__005873f0(DAT_0080ab24,0x200,local_308,0x100,local_51c,0x100,DAT_0080a904,0);
    for (local_520 = 0; local_520 < 0x100; local_520 = local_520 + 1) {
      if ((local_208[local_520] & 1) == 0) {
        if ((local_208[local_520] & 2) == 0) {
          (&DAT_0080a920)[local_520] = 0;
        }
        else {
          (&DAT_0080aa21)[local_520] = (&DAT_0080aa21)[local_520] | 0x20;
          (&DAT_0080a920)[local_520] = local_51c[local_520];
        }
      }
      else {
        (&DAT_0080aa21)[local_520] = (&DAT_0080aa21)[local_520] | 0x10;
        (&DAT_0080a920)[local_520] = local_41c[local_520];
      }
    }
  }
  else {
    for (local_520 = 0; local_520 < 0x100; local_520 = local_520 + 1) {
      if ((local_520 < 0x41) || (0x5a < local_520)) {
        if ((local_520 < 0x61) || (0x7a < local_520)) {
          (&DAT_0080a920)[local_520] = 0;
        }
        else {
          (&DAT_0080aa21)[local_520] = (&DAT_0080aa21)[local_520] | 0x20;
          (&DAT_0080a920)[local_520] = (char)local_520 + -0x20;
        }
      }
      else {
        (&DAT_0080aa21)[local_520] = (&DAT_0080aa21)[local_520] | 0x10;
        (&DAT_0080a920)[local_520] = (char)local_520 + ' ';
      }
    }
  }
  return;
}

