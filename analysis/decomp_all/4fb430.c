
void FUN__text__004fb430(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_80 [16];
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  uint local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_80;
  for (iVar1 = 0x1f; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004fc1d0();
  FUN__text__00422360(0);
  FUN__text__00416a10(local_8 + 0x1e0);
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__00415420();
  local_10 = 0;
  local_14 = 0;
  local_18 = 0;
  local_1c = 0;
  local_20 = 0;
  local_24 = 0;
  local_28 = 0;
  FUN__text__00504830();
  FUN__text__00415420();
  FUN__text__004db060(0x21,0);
  while (iVar1 = FUN__text__0041e3d0(), iVar1 == 0) {
    FUN__text__00422360(0);
  }
  FUN__text__00415420();
  do {
    local_10 = local_10 + 1;
    if (local_18 < 1) {
      local_18 = local_18 + 1;
    }
    else {
      local_18 = 0;
    }
    if (local_1c < 2) {
      local_1c = local_1c + 1;
    }
    else {
      local_1c = 0;
    }
    if (local_20 < 3) {
      local_20 = local_20 + 1;
    }
    else {
      local_20 = 0;
    }
    if (local_24 < 4) {
      local_24 = local_24 + 1;
    }
    else {
      local_24 = 0;
    }
    if (local_28 < 5) {
      local_28 = local_28 + 1;
    }
    else {
      local_28 = 0;
    }
    local_2c = (uint)*(byte *)(local_8 + 0x31);
    switch(local_2c) {
    case 0:
      for (local_c = 0; local_c < 0x14; local_c = local_c + 1) {
        FUN__text__00410310(*(undefined2 *)(&DAT_00757850 + local_c * 0xc),
                            *(undefined2 *)(&DAT_00757852 + local_c * 0xc),
                            *(undefined2 *)(&DAT_00757854 + local_c * 0xc),
                            *(undefined2 *)(&DAT_00757856 + local_c * 0xc),
                            CONCAT22((short)((uint)(local_c * 0xc) >> 0x10),
                                     *(undefined2 *)(&DAT_00757858 + local_c * 0xc)),
                            (uint)*(ushort *)(&DAT_0075785a + local_c * 0xc) << 0x18,1);
      }
      local_30 = local_10;
      if (local_10 < 0x1aad) {
        if (local_10 == 0x1aac) {
          *(undefined1 *)(local_8 + 0x168) = 1;
        }
        else if (local_10 < 0xc9d) {
          if (local_10 == 0xc9c) {
            *(undefined1 *)(local_8 + 0x15c) = 1;
          }
          else if (local_10 < 0x5dd) {
            if (local_10 == 0x5dc) {
              *(undefined1 *)(local_8 + 0x156) = 1;
            }
            else if (local_10 < 0x39d) {
              if (local_10 == 0x39c) {
                *(undefined1 *)(local_8 + 0x153) = 1;
              }
              else if (local_10 == 0x3c) {
                *(undefined1 *)(local_8 + 0x150) = 1;
              }
              else if (local_10 == 0x114) {
                *(undefined1 *)(local_8 + 0x151) = 1;
              }
              else if (local_10 == 0x234) {
                *(undefined1 *)(local_8 + 0x152) = 1;
              }
            }
            else if (local_10 == 0x42c) {
              *(undefined1 *)(local_8 + 0x154) = 1;
            }
            else if (local_10 == 0x4bc) {
              *(undefined1 *)(local_8 + 0x155) = 1;
            }
          }
          else if (local_10 < 0x93d) {
            if (local_10 == 0x93c) {
              *(undefined1 *)(local_8 + 0x159) = 1;
            }
            else if (local_10 == 0x6fc) {
              *(undefined1 *)(local_8 + 0x157) = 1;
            }
            else if (local_10 == 0x81c) {
              *(undefined1 *)(local_8 + 0x158) = 1;
            }
          }
          else if (local_10 == 0xa5c) {
            *(undefined1 *)(local_8 + 0x15a) = 1;
          }
          else if (local_10 == 0xb7c) {
            *(undefined1 *)(local_8 + 0x15b) = 1;
          }
        }
        else if (local_10 < 0x13a7) {
          if (local_10 == 0x13a6) {
            *(undefined1 *)(local_8 + 0x162) = 1;
          }
          else if (local_10 < 0xffd) {
            if (local_10 == 0xffc) {
              *(undefined1 *)(local_8 + 0x15f) = 1;
            }
            else if (local_10 == 0xdbc) {
              *(undefined1 *)(local_8 + 0x15d) = 1;
            }
            else if (local_10 == 0xedc) {
              *(undefined1 *)(local_8 + 0x15e) = 1;
            }
          }
          else if (local_10 == 0x111c) {
            *(undefined1 *)(local_8 + 0x160) = 1;
          }
          else if (local_10 == 0x123c) {
            *(undefined1 *)(local_8 + 0x161) = 1;
          }
        }
        else if (local_10 < 0x174d) {
          if (local_10 == 0x174c) {
            *(undefined1 *)(local_8 + 0x165) = 1;
          }
          else if (local_10 == 0x1434) {
            *(undefined1 *)(local_8 + 0x163) = 1;
          }
          else if (local_10 == 0x162c) {
            *(undefined1 *)(local_8 + 0x164) = 1;
          }
        }
        else if (local_10 == 0x186c) {
          *(undefined1 *)(local_8 + 0x166) = 1;
        }
        else if (local_10 == 0x198c) {
          *(undefined1 *)(local_8 + 0x167) = 1;
        }
      }
      else if (local_10 < 0x2939) {
        if (local_10 == 0x2938) {
          *(undefined1 *)(local_8 + 0x174) = 1;
        }
        else if (local_10 < 0x21fd) {
          if (local_10 == 0x21fc) {
            *(undefined1 *)(local_8 + 0x16e) = 1;
          }
          else if (local_10 < 0x1e0d) {
            if (local_10 == 0x1e0c) {
              *(undefined1 *)(local_8 + 0x16b) = 1;
            }
            else if (local_10 == 0x1bcc) {
              *(undefined1 *)(local_8 + 0x169) = 1;
            }
            else if (local_10 == 0x1cec) {
              *(undefined1 *)(local_8 + 0x16a) = 1;
            }
          }
          else if (local_10 == 0x1fbc) {
            *(undefined1 *)(local_8 + 0x16c) = 1;
          }
          else if (local_10 == 0x20dc) {
            *(undefined1 *)(local_8 + 0x16d) = 1;
          }
        }
        else if (local_10 < 0x25a5) {
          if (local_10 == 0x25a4) {
            *(undefined1 *)(local_8 + 0x171) = 1;
          }
          else if (local_10 == 0x231c) {
            *(undefined1 *)(local_8 + 0x16f) = 1;
          }
          else if (local_10 == 0x243c) {
            *(undefined1 *)(local_8 + 0x170) = 1;
          }
        }
        else if (local_10 == 0x26c4) {
          *(undefined1 *)(local_8 + 0x172) = 1;
        }
        else if (local_10 == 0x27e4) {
          *(undefined1 *)(local_8 + 0x173) = 1;
        }
      }
      else if (local_10 < 0x3281) {
        if (local_10 == 0x3280) {
          *(undefined1 *)(local_8 + 0x17a) = 1;
        }
        else if (local_10 < 0x2ce1) {
          if (local_10 == 0x2ce0) {
            *(undefined1 *)(local_8 + 0x177) = 1;
          }
          else if (local_10 == 0x2a58) {
            *(undefined1 *)(local_8 + 0x175) = 1;
          }
          else if (local_10 == 0x2bc0) {
            *(undefined1 *)(local_8 + 0x176) = 1;
          }
        }
        else if (local_10 == 0x2e48) {
          *(undefined1 *)(local_8 + 0x178) = 1;
        }
        else if (local_10 == 0x3160) {
          *(undefined1 *)(local_8 + 0x179) = 1;
        }
      }
      else if (local_10 < 0x3629) {
        if (local_10 == 0x3628) {
          *(undefined1 *)(local_8 + 0x17d) = 1;
        }
        else if (local_10 == 0x33e8) {
          *(undefined1 *)(local_8 + 0x17b) = 1;
        }
        else if (local_10 == 0x3508) {
          *(undefined1 *)(local_8 + 0x17c) = 1;
        }
      }
      else if (local_10 == 0x3aa2) {
        *(undefined1 *)(local_8 + 0x17e) = 1;
      }
      else if (local_10 == 0x3bc2) {
        *(undefined1 *)(local_8 + 0x17f) = 1;
      }
      FUN__text__004ff070();
      if (local_18 == 0) {
        FUN__text__004fe1a0();
      }
      break;
    case 1:
      if (local_10 < 0x45ff) {
        if (local_10 == 0x45fe) {
          *(undefined1 *)(local_8 + 0x39) = 3;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0xff;
        }
        else if (local_10 == 0x432d) {
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0;
        }
        else if (local_10 == 0x43a5) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
      }
      else if (local_10 == 0x463a) {
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
      }
      local_34 = local_10;
      FUN__text__004fde30();
      if (local_18 == 0) {
        FUN__text__004fdca0();
        FUN__text__004fdd70();
      }
      break;
    case 2:
      if (local_10 == 0x46b2) {
        *(undefined1 *)(local_8 + 0xea) = 1;
        *(undefined2 *)(local_8 + 0xf2) = 0;
        *(undefined1 *)(local_8 + 0x102) = 0;
      }
      else if (local_10 == 0x4ab8) {
        *(undefined1 *)(local_8 + 0xea) = 3;
        *(undefined2 *)(local_8 + 0xf2) = 0;
        *(undefined1 *)(local_8 + 0x102) = 0xff;
      }
      local_38 = local_10;
      FUN__text__004fdb70();
      if (local_18 == 0) {
        FUN__text__004fda40();
        FUN__text__004fdae0();
      }
      break;
    case 3:
      if (local_10 < 0x51fd) {
        if (local_10 == 0x51fc) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
        }
        else if (local_10 < 0x4eb5) {
          if (local_10 == 0x4eb4) {
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
          }
          else if (local_10 == 0x4b6c) {
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
          else if (local_10 == 0x4d10) {
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
          }
        }
        else if (local_10 == 0x5058) {
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0;
        }
        else if (local_10 == 0x510c) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
        }
      }
      else if (local_10 < 0x57d9) {
        if (local_10 == 0x57d8) {
          *(undefined1 *)(local_8 + 0x41) = 1;
          *(undefined1 *)(local_8 + 0x59) = 0;
          *(undefined1 *)(local_8 + 0x71) = 0;
        }
        else if (local_10 == 0x52ec) {
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined1 *)(local_8 + 0x6f) = 0;
        }
        else if (local_10 == 0x5508) {
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined1 *)(local_8 + 0x70) = 0;
        }
      }
      else if (local_10 == 0x597c) {
        *(undefined1 *)(local_8 + 0x42) = 1;
        *(undefined1 *)(local_8 + 0x5a) = 0;
        *(undefined1 *)(local_8 + 0x72) = 0;
      }
      else if (local_10 == 0x5b98) {
        *(undefined1 *)(local_8 + 0x39) = 3;
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x3b) = 3;
        *(undefined1 *)(local_8 + 0x3c) = 3;
        *(undefined1 *)(local_8 + 0x3d) = 3;
        *(undefined1 *)(local_8 + 0x3e) = 3;
        *(undefined1 *)(local_8 + 0x3f) = 3;
        *(undefined1 *)(local_8 + 0x40) = 3;
        *(undefined1 *)(local_8 + 0x41) = 3;
        *(undefined1 *)(local_8 + 0x42) = 3;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x54) = 0;
        *(undefined1 *)(local_8 + 0x55) = 0;
        *(undefined1 *)(local_8 + 0x56) = 0;
        *(undefined1 *)(local_8 + 0x57) = 0;
        *(undefined1 *)(local_8 + 0x58) = 0;
        *(undefined1 *)(local_8 + 0x59) = 0;
        *(undefined1 *)(local_8 + 0x5a) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0xff;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
        *(undefined1 *)(local_8 + 0x6b) = 0xff;
        *(undefined1 *)(local_8 + 0x6c) = 0xff;
        *(undefined1 *)(local_8 + 0x6d) = 0xff;
        *(undefined1 *)(local_8 + 0x6e) = 0xff;
        *(undefined1 *)(local_8 + 0x6f) = 0xff;
        *(undefined1 *)(local_8 + 0x70) = 0xff;
        *(undefined1 *)(local_8 + 0x71) = 0xff;
        *(undefined1 *)(local_8 + 0x72) = 0xff;
      }
      local_3c = local_10;
      FUN__text__004fca10();
      if (local_18 == 0) {
        FUN__text__004fc240();
        FUN__text__004fc570();
      }
      break;
    case 4:
      local_40 = local_10;
      if (local_10 == 0x5d00) {
        *(undefined1 *)(local_8 + 0x31) = 100;
      }
      break;
    case 100:
      FUN__text__00422360(0);
      FUN__text__00422360(0);
      FUN__text__0041e500();
      FUN__text__0041e500();
      FUN__text__0041f4e0(10);
      for (local_c = 0; local_c != 10; local_c = local_c + 1) {
        FUN__text__00464d30();
      }
      FUN__text__00439e30(9);
      local_8 = 0x4fc13a;
      FUN__text__0056ce80();
      return;
    }
    FUN__text__00422360(0);
  } while( true );
}

