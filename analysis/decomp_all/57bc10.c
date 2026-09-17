
undefined4 FUN__text__0057bc10(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  byte *local_2c;
  uint local_28;
  uint local_24;
  byte local_1e [14];
  uint local_10;
  byte *local_c;
  uint local_8;
  
  FUN__text__00577040(0x19);
  iVar1 = getSystemCP(param_1);
  if (iVar1 == DAT_0080a904) {
    FUN__text__005770e0(0x19);
    uVar2 = 0;
  }
  else if (iVar1 == 0) {
    setSBCS();
    FUN__text__0057c0c0();
    FUN__text__005770e0(0x19);
    uVar2 = 0;
  }
  else {
    for (local_8 = 0; local_8 < 5; local_8 = local_8 + 1) {
      if (*(int *)(&DAT_00764388 + local_8 * 0x30) == iVar1) {
        for (local_28 = 0; local_28 < 0x101; local_28 = local_28 + 1) {
          (&DAT_0080aa20)[local_28] = 0;
        }
        for (local_10 = 0; local_10 < 4; local_10 = local_10 + 1) {
          for (local_c = &DAT_00764398 + local_10 * 8 + local_8 * 0x30;
              (*local_c != 0 && (local_c[1] != 0)); local_c = local_c + 2) {
            for (local_28 = (uint)*local_c; local_28 <= local_c[1]; local_28 = local_28 + 1) {
              (&DAT_0080aa21)[local_28] = (&DAT_0080aa21)[local_28] | (&DAT_00764380)[local_10];
            }
          }
        }
        DAT_0080a91c = 1;
        DAT_0080a904 = iVar1;
        DAT_0080ab24 = FUN__text__0057bfc0(iVar1);
        for (local_10 = 0; local_10 < 6; local_10 = local_10 + 1) {
          *(undefined2 *)(&DAT_0080a910 + local_10 * 2) =
               *(undefined2 *)(&DAT_0076438c + local_10 * 2 + local_8 * 0x30);
        }
        FUN__text__0057c0c0();
        FUN__text__005770e0(0x19);
        return 0;
      }
    }
    iVar3 = (*API_KERNEL32_DLL_GetCPInfo)(iVar1,&local_24);
    if (iVar3 == 1) {
      for (local_28 = 0; local_28 < 0x101; local_28 = local_28 + 1) {
        (&DAT_0080aa20)[local_28] = 0;
      }
      DAT_0080ab24 = 0;
      if (local_24 < 2) {
        DAT_0080a91c = 0;
        DAT_0080a904 = iVar1;
      }
      else {
        DAT_0080a904 = iVar1;
        for (local_2c = local_1e; (*local_2c != 0 && (local_2c[1] != 0)); local_2c = local_2c + 2) {
          for (local_28 = (uint)*local_2c; local_28 <= local_2c[1]; local_28 = local_28 + 1) {
            (&DAT_0080aa21)[local_28] = (&DAT_0080aa21)[local_28] | 4;
          }
        }
        for (local_28 = 1; local_28 < 0xff; local_28 = local_28 + 1) {
          (&DAT_0080aa21)[local_28] = (&DAT_0080aa21)[local_28] | 8;
        }
        DAT_0080ab24 = FUN__text__0057bfc0(DAT_0080a904);
        DAT_0080a91c = 1;
      }
      for (local_10 = 0; local_10 < 6; local_10 = local_10 + 1) {
        *(undefined2 *)(&DAT_0080a910 + local_10 * 2) = 0;
      }
      FUN__text__0057c0c0();
      FUN__text__005770e0(0x19);
      uVar2 = 0;
    }
    else if (DAT_0080a4f8 == 0) {
      FUN__text__005770e0(0x19);
      uVar2 = 0xffffffff;
    }
    else {
      setSBCS();
      FUN__text__0057c0c0();
      FUN__text__005770e0(0x19);
      uVar2 = 0;
    }
  }
  return uVar2;
}

