
void FUN__text__005063a0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_c4 [16];
  int local_84;
  int local_80;
  int local_7c;
  int local_78;
  int local_74;
  int local_70;
  int local_6c;
  int local_68;
  int local_64;
  int local_60;
  int local_5c;
  int local_58;
  int local_54;
  int local_50;
  int local_4c;
  int local_48;
  int local_44;
  int local_40;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  uint local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_c4;
  for (iVar1 = 0x30; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00415480(1,0x3c);
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__00416370(0x1b8,0x17c,0,"Now Loading ...",0xffffffff);
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__0050af40();
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__00416370(0x1b8,0x17c,0,"Please Wait ...",0xffffffff);
  FUN__text__00415420();
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
  FUN__text__00505df0();
  FUN__text__00525060();
  FUN__text__00409ef0(local_8 + 0x5a8);
  FUN__text__00409ff0(local_8 + 0x5a8,0,2,0x80);
  FUN__text__00415420();
  FUN__text__004db060(0x1f,0);
  while (iVar1 = FUN__text__0041e3d0(), iVar1 == 0) {
    FUN__text__00422360(0);
  }
  FUN__text__00415420();
  do {
    if (*(byte *)(local_8 + 0x30) < 4) {
      for (local_c = 0; local_c < 2; local_c = local_c + 1) {
        FUN__text__00410310(*(undefined2 *)(&DAT_007587f8 + local_c * 10),
                            *(undefined2 *)(&DAT_007587fa + local_c * 10),
                            *(undefined2 *)(&DAT_007587fc + local_c * 10),
                            *(undefined2 *)(&DAT_007587fe + local_c * 10),
                            *(undefined2 *)(&DAT_00758800 + local_c * 10),0xff000000,0);
      }
    }
    else {
      for (local_c = 2; local_c < 4; local_c = local_c + 1) {
        FUN__text__00410310(*(undefined2 *)(&DAT_007587f8 + local_c * 10),
                            *(undefined2 *)(&DAT_007587fa + local_c * 10),
                            *(undefined2 *)(&DAT_007587fc + local_c * 10),
                            *(undefined2 *)(&DAT_007587fe + local_c * 10),
                            *(undefined2 *)(&DAT_00758800 + local_c * 10),0xff000000,0);
      }
    }
    iVar1 = local_10 + 1;
    if (local_14 < 1) {
      local_14 = local_14 + 1;
    }
    else {
      local_14 = 0;
    }
    if (local_18 < 2) {
      local_18 = local_18 + 1;
    }
    else {
      local_18 = 0;
    }
    if (local_1c < 3) {
      local_1c = local_1c + 1;
    }
    else {
      local_1c = 0;
    }
    if (local_20 < 4) {
      local_20 = local_20 + 1;
    }
    else {
      local_20 = 0;
    }
    if (local_24 < 5) {
      local_24 = local_24 + 1;
    }
    else {
      local_24 = 0;
    }
    local_28 = (uint)*(byte *)(local_8 + 0x30);
    switch(local_28) {
    case 0:
      local_2c = local_10 + -0x1d;
      switch(local_10) {
      case 0x1d:
        *(undefined1 *)(local_8 + 0x39) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
        break;
      case 0x3b:
        *(undefined1 *)(local_8 + 0x3a) = 1;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0;
        break;
      case 0x3f:
        *(undefined1 *)(local_8 + 0x3b) = 1;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0;
        break;
      case 0xa5:
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
        break;
      case 0xa9:
        *(undefined1 *)(local_8 + 0x3b) = 3;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0xff;
        break;
      case 0xbd:
        *(undefined1 *)(local_8 + 0x39) = 3;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0xff;
      }
      local_10 = iVar1;
      FUN__text__005247b0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__005246a0();
        FUN__text__00524580();
        iVar1 = local_10;
      }
      break;
    case 1:
      local_30 = iVar1;
      if (iVar1 < 0x9b5) {
        if (iVar1 == 0x9b4) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
        else if (iVar1 < 0x501) {
          if (iVar1 == 0x500) {
            *(undefined1 *)(local_8 + 0x3a) = 3;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0xff;
          }
          else if (iVar1 < 0x2ef) {
            if (iVar1 == 0x2ee) {
              *(undefined1 *)(local_8 + 0x3b) = 1;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0;
            }
            else if (iVar1 < 0x19b) {
              if (iVar1 == 0x19a) {
                *(undefined1 *)(local_8 + 0x39) = 3;
                *(undefined1 *)(local_8 + 0x51) = 0;
                *(undefined1 *)(local_8 + 0x69) = 0xff;
              }
              else if (iVar1 == 0x136) {
                *(undefined1 *)(local_8 + 0x33) = 1;
                *(undefined1 *)(local_8 + 0x39) = 1;
                *(undefined1 *)(local_8 + 0x51) = 0;
                *(undefined1 *)(local_8 + 0x69) = 0;
              }
              else if (iVar1 == 0x154) {
                *(undefined1 *)(local_8 + 0x35) = 1;
                *(undefined1 *)(local_8 + 0xea) = 1;
                *(undefined2 *)(local_8 + 0xf2) = 0;
                *(undefined2 *)(local_8 + 0x11a) = DAT_007579ce;
              }
            }
            else if (iVar1 == 0x1ae) {
              *(undefined1 *)(local_8 + 0x3a) = 1;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0;
            }
            else if (iVar1 == 0x2da) {
              *(undefined1 *)(local_8 + 0x3a) = 3;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0xff;
            }
          }
          else {
            local_30 = local_10 + -0x397;
            switch(local_10) {
            case 0x397:
              *(undefined1 *)(local_8 + 0x3b) = 3;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0xff;
              break;
            case 0x3c9:
              *(undefined1 *)(local_8 + 0x33) = 2;
              *(undefined1 *)(local_8 + 0x39) = 1;
              *(undefined1 *)(local_8 + 0x51) = 0;
              *(undefined1 *)(local_8 + 0x69) = 0;
              break;
            case 0x45f:
              *(undefined1 *)(local_8 + 0x39) = 3;
              *(undefined1 *)(local_8 + 0x51) = 0;
              *(undefined1 *)(local_8 + 0x69) = 0xff;
              break;
            case 0x473:
              *(undefined1 *)(local_8 + 0x3a) = 1;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0;
            }
          }
        }
        else if (iVar1 < 0x6eb) {
          if (iVar1 == 0x6ea) {
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
          }
          else if (iVar1 < 0x62d) {
            if (iVar1 == 0x62c) {
              *(undefined1 *)(local_8 + 0x3a) = 1;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0;
            }
            else if (iVar1 == 0x532) {
              *(undefined1 *)(local_8 + 0x33) = 3;
              *(undefined1 *)(local_8 + 0x39) = 1;
              *(undefined1 *)(local_8 + 0x51) = 0;
              *(undefined1 *)(local_8 + 0x69) = 0;
            }
            else if (iVar1 == 0x618) {
              *(undefined1 *)(local_8 + 0x39) = 3;
              *(undefined1 *)(local_8 + 0x51) = 0;
              *(undefined1 *)(local_8 + 0x69) = 0xff;
            }
          }
          else if (iVar1 == 0x6d6) {
            *(undefined1 *)(local_8 + 0x3a) = 3;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0xff;
          }
        }
        else if (iVar1 < 0x91b) {
          if (iVar1 == 0x91a) {
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
          }
          else if (iVar1 == 0x7e4) {
            *(undefined1 *)(local_8 + 0x3b) = 3;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0xff;
          }
          else if (iVar1 == 0x816) {
            *(undefined1 *)(local_8 + 0x33) = 4;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
        }
        else if (iVar1 == 0x92e) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
      }
      else if (iVar1 < 0xe2f) {
        if (iVar1 == 0xe2e) {
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
        }
        else if (iVar1 < 0xc27) {
          if (iVar1 == 0xc26) {
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
          }
          else if (iVar1 < 0xa83) {
            if (iVar1 == 0xa82) {
              *(undefined1 *)(local_8 + 0x3c) = 1;
              *(undefined1 *)(local_8 + 0x54) = 0;
              *(undefined1 *)(local_8 + 0x6c) = 0;
            }
            else if (iVar1 == 0x9ce) {
              *(undefined1 *)(local_8 + 0x3b) = 1;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0;
            }
            else if (iVar1 == 0xa6e) {
              *(undefined1 *)(local_8 + 0x3b) = 3;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0xff;
            }
          }
          else if (iVar1 == 0xb2c) {
            *(undefined1 *)(local_8 + 0x3c) = 3;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0xff;
          }
          else if (iVar1 == 0xb5e) {
            *(undefined1 *)(local_8 + 0x33) = 5;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
        }
        else if (iVar1 < 0xcf9) {
          if (iVar1 == 0xcf8) {
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
          }
          else if (iVar1 == 0xc58) {
            *(undefined1 *)(local_8 + 0x33) = 6;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
          else if (iVar1 == 0xce4) {
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
          }
        }
        else if (iVar1 == 0xe1a) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
      }
      else if (iVar1 < 0x1091) {
        if (iVar1 == 0x1090) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
        else {
          local_30 = local_10 + -0xf09;
          switch(local_10) {
          case 0xf09:
            *(undefined1 *)(local_8 + 0x3b) = 3;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0xff;
            break;
          case 0xf3b:
            *(undefined1 *)(local_8 + 0x33) = 7;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            break;
          case 3999:
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
            break;
          case 0xfb3:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
          }
        }
      }
      else {
        local_30 = local_10 + -0x10a3;
        switch(local_10) {
        case 0x10a3:
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
          break;
        case 0x10fd:
          *(undefined1 *)(local_8 + 0x3b) = 3;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0xff;
          break;
        case 0x1111:
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0;
          break;
        case 0x116b:
          *(undefined1 *)(local_8 + 0x3c) = 3;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0xff;
        }
      }
      local_10 = iVar1;
      FUN__text__005224e0();
      FUN__text__0051e2b0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__00521e50();
        FUN__text__00521780();
        FUN__text__0051ca00();
        FUN__text__0051c6c0();
        FUN__text__0051d1d0();
        iVar1 = local_10;
      }
      break;
    case 2:
      if (iVar1 < 0x1331) {
        local_34 = iVar1;
        if (iVar1 == 0x1330) {
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined2 *)(local_8 + 0x82) = DAT_00757f1c;
          *(undefined2 *)(local_8 + 0x9c) = DAT_00757f1e;
        }
        else if (iVar1 < 0x1287) {
          if (iVar1 == 0x1286) {
            *(undefined1 *)(local_8 + 0xed) = 1;
            *(undefined2 *)(local_8 + 0xf8) = 0;
            *(undefined2 *)(local_8 + 0x120) = DAT_00757aae;
          }
          else if (iVar1 == 0x11f0) {
            *(undefined1 *)(local_8 + 0x38) = 1;
            *(undefined1 *)(local_8 + 0x142) = 1;
            *(undefined2 *)(local_8 + 0x144) = 0;
            *(undefined2 *)(local_8 + 0x14c) = 0;
          }
          else if (iVar1 == 0x1254) {
            *(undefined1 *)(local_8 + 0xeb) = 1;
            *(undefined2 *)(local_8 + 0xf4) = 0;
            *(undefined2 *)(local_8 + 0x11c) = DAT_007579de;
          }
          else if (iVar1 == 0x1284) {
            *(undefined1 *)(local_8 + 0xec) = 1;
            *(undefined2 *)(local_8 + 0xf6) = 0;
            *(undefined2 *)(local_8 + 0x11e) = DAT_00757a5e;
          }
        }
        else if (iVar1 == 0x12d2) {
          *(undefined1 *)(local_8 + 0xee) = 1;
          *(undefined2 *)(local_8 + 0xfa) = 0;
          *(undefined2 *)(local_8 + 0x122) = DAT_00757abe;
        }
        else if (iVar1 == 0x1302) {
          *(undefined1 *)(local_8 + 0xef) = 1;
          *(undefined2 *)(local_8 + 0xfc) = 0;
          *(undefined2 *)(local_8 + 0x124) = DAT_00757ace;
        }
        else if (iVar1 == 0x1320) {
          *(undefined1 *)(local_8 + 0x37) = 1;
          *(undefined1 *)(local_8 + 0x12a) = 1;
          *(undefined2 *)(local_8 + 0x12e) = 0;
          *(undefined1 *)(local_8 + 300) = 0;
        }
      }
      else {
        local_34 = local_10 + -0x1333;
        switch(local_10) {
        case 0x1333:
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined2 *)(local_8 + 0x84) = DAT_00757f2c;
          *(undefined2 *)(local_8 + 0x9e) = DAT_00757f2e;
          break;
        case 0x1335:
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined2 *)(local_8 + 0x86) = DAT_00757f3c;
          *(undefined2 *)(local_8 + 0xa0) = PTR_DAT_00757f3e._0_2_;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined2 *)(local_8 + 0x88) = DAT_00757f4c;
          *(undefined2 *)(local_8 + 0xa2) = DAT_00757f4e;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined2 *)(local_8 + 0x8a) = DAT_00757f5c;
          *(undefined2 *)(local_8 + 0xa4) = DAT_00757f5e;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_00757f6c;
          *(undefined2 *)(local_8 + 0xa6) = DAT_00757f6e;
          break;
        case 0x1337:
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined2 *)(local_8 + 0x8e) = DAT_00757f7c;
          *(undefined2 *)(local_8 + 0xa8) = DAT_00757f7e;
          break;
        case 0x1339:
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined2 *)(local_8 + 0x90) = DAT_00757f8c;
          *(undefined2 *)(local_8 + 0xaa) = DAT_00757f8e;
          *(undefined1 *)(local_8 + 0x59) = 0;
          *(undefined2 *)(local_8 + 0x92) = DAT_00757f9c;
          *(undefined2 *)(local_8 + 0xac) = DAT_00757f9e;
          break;
        case 0x133b:
          *(undefined1 *)(local_8 + 0x42) = 1;
          *(undefined1 *)(local_8 + 0x5a) = 0;
          *(undefined2 *)(local_8 + 0x94) = DAT_00757fac;
          *(undefined2 *)(local_8 + 0xae) = DAT_00757fae;
          break;
        case 0x133d:
          *(undefined1 *)(local_8 + 0x43) = 1;
          *(undefined1 *)(local_8 + 0x5b) = 0;
          *(undefined2 *)(local_8 + 0x96) = DAT_00757fbc;
          *(undefined2 *)(local_8 + 0xb0) = DAT_00757fbe;
          *(undefined2 *)(local_8 + 0xca) = 0x153;
          *(undefined2 *)(local_8 + 0xe4) = 0x1a;
          *(undefined1 *)(local_8 + 0x44) = 1;
          *(undefined1 *)(local_8 + 0x5c) = 0;
          *(undefined2 *)(local_8 + 0x98) = DAT_00757adc;
          *(undefined2 *)(local_8 + 0xb2) = DAT_00757ade;
          *(undefined2 *)(local_8 + 0xcc) = 0x200;
          *(undefined2 *)(local_8 + 0xe6) = 0x180;
          break;
        case 0x1347:
          *(undefined1 *)(local_8 + 0x45) = 1;
          *(undefined1 *)(local_8 + 0x5d) = 0;
          *(undefined2 *)(local_8 + 0x9a) = DAT_00757aec;
          *(undefined2 *)(local_8 + 0xce) = 300;
          *(undefined2 *)(local_8 + 0xe8) = 300;
        }
      }
      local_10 = iVar1;
      FUN__text__00524f20();
      FUN__text__0051e2b0();
      FUN__text__0051a760();
      FUN__text__0051b9c0();
      if (local_14 == 0) {
        FUN__text__0051ca00();
        FUN__text__0051c6c0();
        FUN__text__0051d1d0();
        FUN__text__00524cb0();
      }
      if (local_18 == 0) {
        FUN__text__0051b380();
      }
      iVar1 = local_10;
      if (local_24 == 0) {
        FUN__text__0051a0b0();
        iVar1 = local_10;
      }
      break;
    case 3:
      if (iVar1 == 0x13b6) {
        *(undefined1 *)(local_8 + 0x36) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
        *(undefined2 *)(local_8 + 0xb6) = 0x24e;
        *(undefined2 *)(local_8 + 0xd0) = 0x1bb;
      }
      local_38 = iVar1;
      local_10 = iVar1;
      FUN__text__00519eb0();
      iVar1 = local_10;
      if (local_18 == 0) {
        FUN__text__00519d90();
        FUN__text__00519d40();
        FUN__text__00519de0();
        iVar1 = local_10;
      }
      break;
    case 4:
      if (iVar1 < 0x161f) {
        local_3c = iVar1;
        if (iVar1 == 0x161e) {
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined2 *)(local_8 + 0x8e) = PTR_DAT_0075862c._0_2_;
        }
        else if (iVar1 < 0x15db) {
          if (iVar1 == 0x15da) {
            *(undefined1 *)(local_8 + 0x12a) = 3;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0xff;
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
            *(undefined1 *)(local_8 + 0xeb) = 1;
            *(undefined1 *)(local_8 + 0xec) = 1;
            *(undefined2 *)(local_8 + 0xf6) = 0;
            *(undefined2 *)(local_8 + 0x10e) = DAT_00757bac;
            *(undefined1 *)(local_8 + 0xed) = 1;
            *(undefined2 *)(local_8 + 0xf8) = 0;
            *(undefined2 *)(local_8 + 0x110) = DAT_00757b2c;
            *(undefined2 *)(local_8 + 0x120) = DAT_00757b2e;
            *(undefined1 *)(local_8 + 0xee) = 1;
            *(undefined2 *)(local_8 + 0xfa) = 0;
            *(undefined2 *)(local_8 + 0x112) = DAT_00757b4c;
            *(undefined2 *)(local_8 + 0x122) = DAT_00757b4e;
            *(undefined1 *)(local_8 + 0xef) = 1;
            *(undefined2 *)(local_8 + 0xfc) = 0;
            *(undefined2 *)(local_8 + 0x114) = DAT_00757b6c;
            *(undefined2 *)(local_8 + 0x124) = DAT_00757b6e;
            *(undefined1 *)(local_8 + 0xf0) = 1;
            *(undefined2 *)(local_8 + 0xfe) = 0;
            *(undefined2 *)(local_8 + 0x116) = DAT_00757b8c;
            *(undefined2 *)(local_8 + 0x126) = DAT_00757b8e;
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined2 *)(local_8 + 0xa0) = 0x115;
            *(undefined1 *)(local_8 + 0x3c) = 1;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined2 *)(local_8 + 0x88) = DAT_007585fc;
            *(undefined2 *)(local_8 + 0xa2) = DAT_007585fe;
          }
          else if (iVar1 == 0x14f0) {
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined2 *)(local_8 + 0x11a) = DAT_00757afe;
            *(undefined1 *)(local_8 + 0x102) = 0;
          }
          else if (iVar1 == 0x157d) {
            *(undefined1 *)(local_8 + 0x37) = 2;
            *(undefined1 *)(local_8 + 0x12a) = 1;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0;
          }
          else if (iVar1 == 0x1589) {
            *(undefined1 *)(local_8 + 0x34) = 1;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
        }
        else if (iVar1 == 0x1606) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined2 *)(local_8 + 0x8a) = PTR_DAT_0075861c._0_2_;
        }
        else if (iVar1 == 0x1616) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_0075860c;
          *(undefined2 *)(local_8 + 0xa6) = DAT_0075860e;
        }
      }
      else {
        local_3c = local_10 + -0x1651;
        switch(local_10) {
        case 0x1651:
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_0075860c;
          *(undefined2 *)(local_8 + 0xa6) = DAT_0075860e;
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined2 *)(local_8 + 0x8e) = PTR_DAT_0075862c._0_2_;
          break;
        case 0x1656:
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined2 *)(local_8 + 0x88) = DAT_007585fc;
          *(undefined2 *)(local_8 + 0xa2) = DAT_007585fe;
          break;
        case 0x1686:
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined2 *)(local_8 + 0x8a) = PTR_DAT_0075861c._0_2_;
          break;
        case 0x168b:
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined2 *)(local_8 + 0x88) = DAT_007585fc;
          *(undefined2 *)(local_8 + 0xa2) = DAT_007585fe;
          break;
        case 0x1694:
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined2 *)(local_8 + 0x90) = PTR_DAT_0075861c._0_2_;
          *(undefined1 *)(local_8 + 299) = 1;
          *(undefined2 *)(local_8 + 0x130) = 0;
          *(undefined1 *)(local_8 + 0x12d) = 0;
          break;
        case 0x1698:
          *(undefined1 *)(local_8 + 0x41) = 1;
          *(undefined1 *)(local_8 + 0x59) = 0;
          *(undefined1 *)(local_8 + 0x71) = 0;
        }
      }
      local_10 = iVar1;
      FUN__text__00519a20();
      FUN__text__0051b9c0();
      FUN__text__00515040();
      FUN__text__00512840();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__00519910();
        FUN__text__00519960();
        FUN__text__0051b380();
        FUN__text__0051afe0();
        FUN__text__00514170();
        FUN__text__00513480();
        FUN__text__005122d0();
        iVar1 = local_10;
      }
      break;
    case 5:
      if (iVar1 == 0x1718) {
        *(undefined1 *)(local_8 + 0x41) = 3;
        *(undefined1 *)(local_8 + 0x59) = 0;
        *(undefined1 *)(local_8 + 0x71) = 0xff;
      }
      else if (iVar1 == 0x1742) {
        *(undefined1 *)(local_8 + 0x35) = 2;
        *(undefined1 *)(local_8 + 0xea) = 1;
        *(undefined2 *)(local_8 + 0xf2) = 0;
        *(undefined1 *)(local_8 + 0x102) = 0;
      }
      local_40 = iVar1;
      local_10 = iVar1;
      FUN__text__00515040();
      FUN__text__0051e2b0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__00513480();
        FUN__text__0051ca00();
        iVar1 = local_10;
      }
      break;
    case 6:
      if (iVar1 < 0x17fc) {
        if (iVar1 == 0x17fb) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
          local_44 = 0x17fb;
        }
        else {
          local_44 = local_10 + -0x1756;
          switch(local_10) {
          case 0x1756:
            *(undefined1 *)(local_8 + 0x34) = 2;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            break;
          case 0x1758:
            *(undefined1 *)(local_8 + 0x3d) = 1;
            *(undefined1 *)(local_8 + 0x55) = 0;
            *(undefined1 *)(local_8 + 0x6d) = 0;
            break;
          case 6000:
            *(undefined1 *)(local_8 + 0xeb) = 1;
            *(undefined2 *)(local_8 + 0xf4) = 0;
            *(undefined1 *)(local_8 + 0x103) = 0;
            break;
          case 0x178c:
            *(undefined1 *)(local_8 + 0xec) = 1;
            *(undefined2 *)(local_8 + 0xf6) = 0;
            *(undefined1 *)(local_8 + 0x104) = 0;
            break;
          case 0x17a6:
            *(undefined1 *)(local_8 + 0xed) = 1;
            *(undefined2 *)(local_8 + 0xf8) = 0;
            *(undefined1 *)(local_8 + 0x105) = 0;
            break;
          case 0x17c0:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            break;
          case 0x17dc:
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
            break;
          case 0x17f8:
            *(undefined1 *)(local_8 + 0x3c) = 1;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0;
          }
        }
      }
      else {
        local_44 = local_10 + -0x1812;
        switch(local_10) {
        case 0x1812:
          *(undefined1 *)(local_8 + 0xee) = 1;
          *(undefined2 *)(local_8 + 0xfa) = 0;
          *(undefined1 *)(local_8 + 0x106) = 0;
          break;
        case 0x182e:
          *(undefined1 *)(local_8 + 0xef) = 1;
          *(undefined2 *)(local_8 + 0xfc) = 0;
          *(undefined1 *)(local_8 + 0x107) = 0;
          break;
        case 0x1838:
          *(undefined1 *)(local_8 + 0x3d) = 3;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0xff;
          break;
        case 0x1848:
          *(undefined1 *)(local_8 + 0xf0) = 1;
          *(undefined2 *)(local_8 + 0xfe) = 0;
          *(undefined1 *)(local_8 + 0x108) = 0;
          break;
        case 0x184e:
          *(undefined1 *)(local_8 + 0x3e) = 3;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0xff;
          break;
        case 0x1864:
          *(undefined1 *)(local_8 + 0xf1) = 1;
          *(undefined2 *)(local_8 + 0x100) = 0;
          *(undefined1 *)(local_8 + 0x109) = 0;
          break;
        case 0x1868:
          *(undefined1 *)(local_8 + 0x37) = 3;
          *(undefined1 *)(local_8 + 0x12a) = 1;
          *(undefined2 *)(local_8 + 0x12e) = 0;
          *(undefined1 *)(local_8 + 300) = 0;
          *(undefined2 *)(local_8 + 0x130) = 0;
          *(undefined2 *)(local_8 + 0x134) = DAT_00758852;
          *(undefined2 *)(local_8 + 0x13a) = DAT_0075884c;
          *(undefined2 *)(local_8 + 0x13c) = DAT_00758856;
        }
      }
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      FUN__text__0051b9c0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051ca00();
        FUN__text__0050b900();
        FUN__text__00514170();
        FUN__text__00513480();
        FUN__text__0051b380();
        FUN__text__0051b8b0();
        iVar1 = local_10;
      }
      break;
    case 7:
      if (iVar1 < 0x1a13) {
        if (iVar1 == 0x1a12) {
          *(undefined1 *)(local_8 + 0xeb) = 1;
          *(undefined2 *)(local_8 + 0xf4) = 0;
          *(undefined1 *)(local_8 + 0x103) = 0;
          *(undefined2 *)(local_8 + 0x10c) = PTR_DAT_00757c5c._0_2_;
        }
        else if (iVar1 < 0x1939) {
          if (iVar1 == 0x1938) {
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
          }
          else if (iVar1 == 0x18a8) {
            *(undefined1 *)(local_8 + 0x35) = 3;
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined1 *)(local_8 + 0x102) = 0;
            *(undefined2 *)(local_8 + 0x10a) = PTR_DAT_00757c4c._0_2_;
          }
          else if (iVar1 == 0x18e5) {
            *(undefined1 *)(local_8 + 0x34) = 3;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            *(undefined2 *)(local_8 + 0x82) = DAT_0075847c;
            *(undefined2 *)(local_8 + 0x9c) = DAT_0075847e;
          }
          else if (iVar1 == 0x18f6) {
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            *(undefined2 *)(local_8 + 0x84) = DAT_0075851c;
            *(undefined2 *)(local_8 + 0x9e) = DAT_0075851e;
          }
        }
        else if (iVar1 == 0x196b) {
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0;
        }
        else if (iVar1 == 0x19e5) {
          *(undefined1 *)(local_8 + 0x3b) = 3;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0xff;
        }
        else if (iVar1 == 0x19ec) {
          *(undefined1 *)(local_8 + 0x3c) = 3;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0xff;
        }
      }
      else if (iVar1 < 0x1b79) {
        if (iVar1 == 0x1b78) {
          *(undefined1 *)(local_8 + 0x3e) = 3;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0xff;
        }
        else if (iVar1 == 0x1a42) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
        }
        else if (iVar1 == 0x1a9f) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
        }
        else if (iVar1 == 0x1b6f) {
          *(undefined1 *)(local_8 + 0x3d) = 3;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0xff;
        }
      }
      else if (iVar1 == 0x1b7e) {
        *(undefined1 *)(local_8 + 0x12a) = 3;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0xff;
      }
      else if (iVar1 == 0x1bb8) {
        *(undefined1 *)(local_8 + 0x3f) = 1;
        *(undefined1 *)(local_8 + 0x57) = 0;
        *(undefined1 *)(local_8 + 0x6f) = 0;
      }
      local_48 = iVar1;
      local_10 = iVar1;
      FUN__text__0051b9c0();
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051b380();
        FUN__text__0051afe0();
        FUN__text__0051b8b0();
        FUN__text__0051ca00();
        FUN__text__0051c6c0();
        FUN__text__0051d1d0();
        FUN__text__0050b900();
        FUN__text__0050afd0();
        FUN__text__0050c6f0();
        FUN__text__00514170();
        FUN__text__00513480();
        iVar1 = local_10;
      }
      break;
    case 8:
      local_4c = iVar1;
      if (iVar1 < 0x1d52) {
        if (iVar1 == 0x1d51) {
          *(undefined1 *)(local_8 + 0x37) = 4;
          *(undefined1 *)(local_8 + 0x12a) = 1;
          *(undefined2 *)(local_8 + 0x12e) = 0;
          *(undefined1 *)(local_8 + 300) = 0;
        }
        else {
          local_4c = local_10 + -0x1c38;
          switch(local_10) {
          case 0x1c38:
            *(undefined1 *)(local_8 + 0x3f) = 3;
            *(undefined1 *)(local_8 + 0x57) = 0;
            *(undefined1 *)(local_8 + 0x6f) = 0xff;
            break;
          case 0x1c5b:
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            *(undefined2 *)(local_8 + 0x82) = DAT_0075852c;
            *(undefined2 *)(local_8 + 0x9c) = DAT_0075852e;
            break;
          case 0x1c5f:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            *(undefined2 *)(local_8 + 0x84) = DAT_007584fc;
            *(undefined2 *)(local_8 + 0x9e) = DAT_007584fe;
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
            break;
          case 0x1cc5:
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined2 *)(local_8 + 0x10a) = PTR_DAT_00757c6c._0_2_;
            break;
          case 0x1d08:
            *(undefined1 *)(local_8 + 0x3b) = 3;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0xff;
          }
        }
      }
      else if (iVar1 < 0x1e6f) {
        if (iVar1 == 0x1e6e) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
        }
        else if (iVar1 == 0x1da2) {
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0;
        }
        else if (iVar1 == 0x1e57) {
          *(undefined1 *)(local_8 + 0x3c) = 3;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0xff;
        }
      }
      else if (iVar1 == 0x1f73) {
        *(undefined1 *)(local_8 + 0x3d) = 3;
        *(undefined1 *)(local_8 + 0x55) = 0;
        *(undefined1 *)(local_8 + 0x6d) = 0xff;
      }
      else if (iVar1 == 0x1fa9) {
        *(undefined1 *)(local_8 + 0x12a) = 3;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0xff;
      }
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      FUN__text__0051b9c0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051b380();
        FUN__text__0051afe0();
        FUN__text__0051c6c0();
        FUN__text__0051d1d0();
        FUN__text__0050b900();
        FUN__text__0050afd0();
        FUN__text__0050c6f0();
        FUN__text__00514170();
        FUN__text__00513480();
        iVar1 = local_10;
      }
      break;
    case 9:
      local_50 = local_10 + -0x1fe2;
      switch(local_10) {
      case 0x1fe2:
        *(undefined1 *)(local_8 + 0x37) = 5;
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x1fe4:
        *(undefined1 *)(local_8 + 0x34) = 5;
        *(undefined1 *)(local_8 + 0x39) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
        *(undefined2 *)(local_8 + 0x82) = PTR_DAT_007583ec._0_2_;
        break;
      case 0x1ffd:
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x1fff:
        *(undefined1 *)(local_8 + 0x3a) = 1;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0;
        *(undefined2 *)(local_8 + 0x84) = PTR_DAT_007583fc._0_2_;
        break;
      case 0x2018:
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x201a:
        *(undefined1 *)(local_8 + 0x3b) = 1;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0;
        *(undefined2 *)(local_8 + 0x86) = PTR_DAT_0075840c._0_2_;
        break;
      case 0x2037:
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x2039:
        *(undefined1 *)(local_8 + 0x3c) = 1;
        *(undefined1 *)(local_8 + 0x54) = 0;
        *(undefined1 *)(local_8 + 0x6c) = 0;
        *(undefined2 *)(local_8 + 0x88) = PTR_DAT_0075841c._0_2_;
        break;
      case 0x2056:
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x2058:
        *(undefined1 *)(local_8 + 0x3d) = 1;
        *(undefined1 *)(local_8 + 0x55) = 0;
        *(undefined1 *)(local_8 + 0x6d) = 0;
        *(undefined2 *)(local_8 + 0x8a) = PTR_DAT_0075842c._0_2_;
        break;
      case 0x206f:
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x2071:
        *(undefined1 *)(local_8 + 0x3e) = 1;
        *(undefined1 *)(local_8 + 0x56) = 0;
        *(undefined1 *)(local_8 + 0x6e) = 0;
        *(undefined2 *)(local_8 + 0x8c) = PTR_DAT_0075843c._0_2_;
        break;
      case 0x2088:
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x208a:
        *(undefined1 *)(local_8 + 0x3f) = 1;
        *(undefined1 *)(local_8 + 0x57) = 0;
        *(undefined1 *)(local_8 + 0x6f) = 0;
        *(undefined2 *)(local_8 + 0x8e) = PTR_DAT_0075844c._0_2_;
        break;
      case 0x20a1:
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
        break;
      case 0x20a3:
        *(undefined1 *)(local_8 + 0x40) = 1;
        *(undefined1 *)(local_8 + 0x58) = 0;
        *(undefined1 *)(local_8 + 0x70) = 0;
        *(undefined2 *)(local_8 + 0x90) = PTR_DAT_0075845c._0_2_;
      }
      local_10 = iVar1;
      FUN__text__0051b9c0();
      FUN__text__0050d5a0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051b380();
        FUN__text__0050b900();
        FUN__text__0050c6f0();
        iVar1 = local_10;
      }
      break;
    case 10:
      if (iVar1 < 0x21ff) {
        if (iVar1 == 0x21fe) {
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
        }
        else if (iVar1 == 0x20e6) {
          *(undefined1 *)(local_8 + 0x35) = 5;
          *(undefined1 *)(local_8 + 0xea) = 1;
          *(undefined2 *)(local_8 + 0xf2) = 0;
          *(undefined1 *)(local_8 + 0x102) = 0;
          *(undefined2 *)(local_8 + 0x11a) = DAT_00757c8e;
          *(undefined1 *)(local_8 + 0xeb) = 1;
          *(undefined2 *)(local_8 + 0xf4) = 0;
          *(undefined1 *)(local_8 + 0x103) = 0;
          *(undefined2 *)(local_8 + 0x11c) = DAT_00757c9e;
          *(undefined1 *)(local_8 + 0xec) = 1;
          *(undefined2 *)(local_8 + 0xf6) = 0;
          *(undefined1 *)(local_8 + 0x104) = 0;
          *(undefined2 *)(local_8 + 0x11e) = DAT_00757cae;
        }
        else if (iVar1 == 0x2190) {
          *(undefined1 *)(local_8 + 0x34) = 6;
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0;
          *(undefined2 *)(local_8 + 0x9c) = DAT_0075823e;
        }
        else if (iVar1 == 0x21d0) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
      }
      else if (iVar1 == 0x2318) {
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
      }
      else if (iVar1 == 0x232a) {
        *(undefined1 *)(local_8 + 0xed) = 2;
        *(undefined2 *)(local_8 + 0xf8) = 0;
        *(undefined1 *)(local_8 + 0x105) = 0xff;
        *(undefined2 *)(local_8 + 0x120) = DAT_00757cbe;
      }
      else if (iVar1 == 0x2334) {
        *(undefined1 *)(local_8 + 0x3b) = 3;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0xff;
      }
      local_54 = iVar1;
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051c6c0();
        FUN__text__0051ca00();
        FUN__text__0051d1d0();
        FUN__text__0050afd0();
        FUN__text__0050b900();
        FUN__text__0050c6f0();
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0xb:
      if (iVar1 < 0x2503) {
        if (iVar1 == 0x2502) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
          *(undefined2 *)(local_8 + 0x8a) = DAT_007584ec;
          *(undefined2 *)(local_8 + 0xa4) = DAT_007584ee;
          local_58 = 0x2502;
        }
        else {
          local_58 = local_10 + -0x241f;
          switch(local_10) {
          case 0x241f:
            *(undefined1 *)(local_8 + 0x34) = 7;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            *(undefined2 *)(local_8 + 0x82) = DAT_0075850c;
            *(undefined2 *)(local_8 + 0x9c) = DAT_0075850e;
            break;
          case 0x2425:
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
            break;
          case 0x244b:
            *(undefined1 *)(local_8 + 0x3c) = 1;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0;
            break;
          case 0x2461:
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined1 *)(local_8 + 0x102) = 0;
            break;
          case 0x2467:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            *(undefined2 *)(local_8 + 0x84) = DAT_007584dc;
            break;
          case 0x24b3:
            *(undefined1 *)(local_8 + 0x3b) = 3;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0xff;
            break;
          case 0x24c1:
            *(undefined1 *)(local_8 + 0x3c) = 3;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0xff;
            break;
          case 0x24cb:
            *(undefined1 *)(local_8 + 0xeb) = 1;
            *(undefined2 *)(local_8 + 0xf4) = 0;
            *(undefined1 *)(local_8 + 0x103) = 0;
          }
        }
      }
      else {
        local_58 = local_10 + -0x2521;
        switch(local_10) {
        case 0x2521:
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined1 *)(local_8 + 0x6f) = 0;
          break;
        case 0x2525:
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_0075846c;
          break;
        case 0x254f:
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined1 *)(local_8 + 0x70) = 0;
          break;
        case 0x2559:
          *(undefined1 *)(local_8 + 0x41) = 1;
          *(undefined1 *)(local_8 + 0x59) = 0;
          *(undefined1 *)(local_8 + 0x71) = 0;
          break;
        case 0x25af:
          *(undefined1 *)(local_8 + 0x3f) = 3;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined1 *)(local_8 + 0x6f) = 0xff;
          break;
        case 0x25dd:
          *(undefined1 *)(local_8 + 0x40) = 3;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined1 *)(local_8 + 0x70) = 0xff;
          break;
        case 0x25e7:
          *(undefined1 *)(local_8 + 0x41) = 3;
          *(undefined1 *)(local_8 + 0x59) = 0;
          *(undefined1 *)(local_8 + 0x71) = 0xff;
          break;
        case 0x2603:
          *(undefined1 *)(local_8 + 0xeb) = 3;
          *(undefined2 *)(local_8 + 0xf4) = 0;
          *(undefined1 *)(local_8 + 0x103) = 0xff;
          *(undefined1 *)(local_8 + 0xec) = 1;
          *(undefined2 *)(local_8 + 0xf6) = 0;
          *(undefined1 *)(local_8 + 0x104) = 0;
          *(undefined2 *)(local_8 + 0x11e) = DAT_00757cce;
        }
      }
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051c6c0();
        FUN__text__0051ca00();
        FUN__text__0051d1d0();
        FUN__text__0050afd0();
        FUN__text__0050b900();
        FUN__text__0050c6f0();
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0xc:
      local_5c = local_10 + -0x2675;
      switch(local_10) {
      case 0x2675:
        *(undefined1 *)(local_8 + 0x34) = 8;
        *(undefined1 *)(local_8 + 0x39) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
        break;
      case 0x2677:
        *(undefined1 *)(local_8 + 0x3a) = 1;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0;
        *(undefined2 *)(local_8 + 0x84) = DAT_0075853c;
        *(undefined2 *)(local_8 + 0x9e) = DAT_0075853e;
        break;
      case 0x268d:
        *(undefined1 *)(local_8 + 0x3b) = 1;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0;
        *(undefined2 *)(local_8 + 0x86) = DAT_0075854c;
        *(undefined2 *)(local_8 + 0xa0) = DAT_0075854e;
        break;
      case 0x2765:
        *(undefined1 *)(local_8 + 0x39) = 3;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0xff;
      }
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051c6c0();
        FUN__text__0051ca00();
        FUN__text__0051d1d0();
        FUN__text__0050afd0();
        FUN__text__0050b900();
        FUN__text__0050c6f0();
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0xd:
      if (iVar1 < 0x28df) {
        if (iVar1 == 0x28de) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
        else if (iVar1 == 0x27dc) {
          *(undefined1 *)(local_8 + 0x34) = 9;
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0;
        }
        else if (iVar1 == 0x28a2) {
          *(undefined1 *)(local_8 + 0x39) = 3;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0xff;
        }
      }
      else if (iVar1 == 0x298c) {
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
      }
      local_60 = iVar1;
      local_10 = iVar1;
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0xe:
      if (iVar1 < 0x2b75) {
        if (iVar1 == 0x2b74) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
        else if (iVar1 == 0x29d4) {
          *(undefined1 *)(local_8 + 0x35) = 8;
          *(undefined1 *)(local_8 + 0xea) = 1;
          *(undefined2 *)(local_8 + 0xf2) = 0;
          *(undefined1 *)(local_8 + 0x102) = 0;
          *(undefined2 *)(local_8 + 0x10a) = PTR_DAT_00757cdc._0_2_;
        }
        else if (iVar1 == 0x2a5b) {
          *(undefined1 *)(local_8 + 0x34) = 10;
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0;
          *(undefined2 *)(local_8 + 0x82) = DAT_007587ec;
          *(undefined2 *)(local_8 + 0x9c) = DAT_007587ee;
        }
        else if (iVar1 == 0x2a9c) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
      }
      else if (iVar1 == 0x2be6) {
        *(undefined1 *)(local_8 + 0x3b) = 1;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0;
      }
      else if (iVar1 == 0x2c9a) {
        *(undefined1 *)(local_8 + 0x3b) = 3;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0xff;
      }
      local_64 = iVar1;
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      if (local_14 == 0) {
        FUN__text__00513480();
        FUN__text__00514170();
      }
      iVar1 = local_10;
      if (local_18 == 0) {
        FUN__text__0051c6c0();
        FUN__text__0051ca00();
        FUN__text__0051d1d0();
        FUN__text__0050afd0();
        FUN__text__0050b900();
        FUN__text__0050c6f0();
        iVar1 = local_10;
      }
      break;
    case 0xf:
      local_68 = iVar1;
      if (iVar1 < 0x2ded) {
        if (iVar1 == 0x2dec) {
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
          *(undefined2 *)(local_8 + 0x86) = DAT_0075855c;
          *(undefined2 *)(local_8 + 0xa0) = DAT_0075855e;
        }
        else {
          local_68 = local_10 + -0x2cd1;
          switch(local_10) {
          case 0x2cd1:
            *(undefined1 *)(local_8 + 0x35) = 9;
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined1 *)(local_8 + 0x102) = 0;
            *(undefined2 *)(local_8 + 0x10a) = PTR_DAT_00757d1c._0_2_;
            break;
          case 0x2ce3:
            *(undefined1 *)(local_8 + 0xeb) = 1;
            *(undefined2 *)(local_8 + 0xf4) = 0;
            *(undefined1 *)(local_8 + 0x103) = 0;
            *(undefined2 *)(local_8 + 0x11c) = DAT_00757cfe;
            break;
          case 0x2d0d:
            *(undefined1 *)(local_8 + 0x34) = 0xb;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            *(undefined2 *)(local_8 + 0x82) = PTR_DAT_0075848c._0_2_;
            break;
          case 0x2d45:
            *(undefined1 *)(local_8 + 0x3f) = 1;
            *(undefined1 *)(local_8 + 0x57) = 0;
            *(undefined1 *)(local_8 + 0x6f) = 0;
            break;
          case 0x2d7d:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            *(undefined2 *)(local_8 + 0x84) = PTR_DAT_0075849c._0_2_;
            break;
          case 0x2d7f:
            *(undefined1 *)(local_8 + 0xec) = 1;
            *(undefined2 *)(local_8 + 0xf6) = 0;
            *(undefined1 *)(local_8 + 0x104) = 0;
            *(undefined2 *)(local_8 + 0x11e) = DAT_00757d0e;
            break;
          case 0x2d91:
            *(undefined1 *)(local_8 + 0xed) = 1;
            *(undefined2 *)(local_8 + 0xf8) = 0;
            *(undefined1 *)(local_8 + 0x105) = 0;
            *(undefined2 *)(local_8 + 0x110) = PTR_DAT_00757d3c._0_2_;
          }
        }
      }
      else if (iVar1 < 0x2e9f) {
        if (iVar1 == 0x2e9e) {
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined1 *)(local_8 + 0x70) = 0;
        }
        else if (iVar1 == 0x2dee) {
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0;
          *(undefined2 *)(local_8 + 0x88) = DAT_0075856c;
          *(undefined2 *)(local_8 + 0xa2) = DAT_0075856e;
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
          *(undefined2 *)(local_8 + 0x8a) = DAT_0075857c;
          *(undefined2 *)(local_8 + 0xa4) = DAT_0075857e;
        }
        else if (iVar1 == 0x2df2) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_0075858c;
          *(undefined2 *)(local_8 + 0xa6) = DAT_0075858e;
        }
        else if (iVar1 == 0x2e52) {
          *(undefined1 *)(local_8 + 0x3f) = 3;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined1 *)(local_8 + 0x6f) = 0xff;
        }
      }
      else if (iVar1 == 0x2f38) {
        *(undefined1 *)(local_8 + 0x40) = 3;
        *(undefined1 *)(local_8 + 0x58) = 0;
        *(undefined1 *)(local_8 + 0x70) = 0xff;
      }
      else if (iVar1 == 0x2f62) {
        *(undefined1 *)(local_8 + 0x41) = 1;
        *(undefined1 *)(local_8 + 0x59) = 0;
        *(undefined1 *)(local_8 + 0x71) = 0;
      }
      else if (iVar1 == 0x2ff8) {
        *(undefined1 *)(local_8 + 0x41) = 3;
        *(undefined1 *)(local_8 + 0x59) = 0;
        *(undefined1 *)(local_8 + 0x71) = 0xff;
      }
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051c6c0();
        FUN__text__0051ca00();
        FUN__text__0051d1d0();
        FUN__text__0050afd0();
        FUN__text__0050b900();
        FUN__text__0050c6f0();
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0x10:
      if (iVar1 < 0x30b3) {
        if (iVar1 == 0x30b2) {
          *(undefined1 *)(local_8 + 0x4a) = 3;
          *(undefined1 *)(local_8 + 0x62) = 0;
          *(undefined1 *)(local_8 + 0x7a) = 0xff;
          local_6c = 0x30b2;
        }
        else {
          local_6c = local_10 + -0x303b;
          switch(local_10) {
          case 0x303b:
            *(undefined1 *)(local_8 + 0x35) = 10;
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined1 *)(local_8 + 0x37) = 6;
            *(undefined1 *)(local_8 + 0x12a) = 3;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0xff;
            break;
          case 0x303f:
            *(undefined1 *)(local_8 + 0x34) = 0xc;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
            *(undefined1 *)(local_8 + 0x3c) = 1;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0;
            *(undefined1 *)(local_8 + 0x3d) = 1;
            *(undefined1 *)(local_8 + 0x55) = 0;
            *(undefined1 *)(local_8 + 0x6d) = 0;
            *(undefined1 *)(local_8 + 0x3e) = 1;
            *(undefined1 *)(local_8 + 0x56) = 0;
            *(undefined1 *)(local_8 + 0x6e) = 0;
            *(undefined1 *)(local_8 + 0x3f) = 1;
            *(undefined1 *)(local_8 + 0x57) = 0;
            *(undefined1 *)(local_8 + 0x6f) = 0;
            *(undefined1 *)(local_8 + 0x40) = 1;
            *(undefined1 *)(local_8 + 0x58) = 0;
            *(undefined1 *)(local_8 + 0x70) = 0;
            *(undefined1 *)(local_8 + 0x41) = 1;
            *(undefined1 *)(local_8 + 0x59) = 0;
            *(undefined1 *)(local_8 + 0x71) = 0;
            *(undefined1 *)(local_8 + 0x42) = 1;
            *(undefined1 *)(local_8 + 0x5a) = 0;
            *(undefined1 *)(local_8 + 0x72) = 0;
            *(undefined1 *)(local_8 + 0x43) = 1;
            *(undefined1 *)(local_8 + 0x5b) = 0;
            *(undefined1 *)(local_8 + 0x73) = 0;
            *(undefined1 *)(local_8 + 0x44) = 1;
            *(undefined1 *)(local_8 + 0x5c) = 0;
            *(undefined1 *)(local_8 + 0x74) = 0;
            *(undefined1 *)(local_8 + 0x45) = 1;
            *(undefined1 *)(local_8 + 0x5d) = 0;
            *(undefined1 *)(local_8 + 0x75) = 0;
            *(undefined1 *)(local_8 + 0x46) = 1;
            *(undefined1 *)(local_8 + 0x5e) = 0;
            *(undefined1 *)(local_8 + 0x76) = 0;
            *(undefined1 *)(local_8 + 0x47) = 1;
            *(undefined1 *)(local_8 + 0x5f) = 0;
            *(undefined1 *)(local_8 + 0x77) = 0;
            *(undefined1 *)(local_8 + 0x48) = 1;
            *(undefined1 *)(local_8 + 0x60) = 0;
            *(undefined1 *)(local_8 + 0x78) = 0;
            *(undefined1 *)(local_8 + 0x49) = 1;
            *(undefined1 *)(local_8 + 0x61) = 0;
            *(undefined1 *)(local_8 + 0x79) = 0;
            *(undefined1 *)(local_8 + 0x4a) = 1;
            *(undefined1 *)(local_8 + 0x62) = 0;
            *(undefined1 *)(local_8 + 0x7a) = 0;
            *(undefined1 *)(local_8 + 0x4b) = 1;
            *(undefined1 *)(local_8 + 99) = 0;
            *(undefined1 *)(local_8 + 0x7b) = 0;
            break;
          case 0x305f:
            *(undefined1 *)(local_8 + 0x4c) = 1;
            *(undefined1 *)(local_8 + 100) = 0;
            *(undefined1 *)(local_8 + 0x7c) = 0;
            break;
          case 0x3065:
            *(undefined1 *)(local_8 + 0x4d) = 1;
            *(undefined1 *)(local_8 + 0x65) = 0;
            *(undefined1 *)(local_8 + 0x7d) = 0;
            break;
          case 0x306b:
            *(undefined1 *)(local_8 + 0x4e) = 1;
            *(undefined1 *)(local_8 + 0x66) = 0;
            *(undefined1 *)(local_8 + 0x7e) = 0;
            break;
          case 0x3071:
            *(undefined1 *)(local_8 + 0x4f) = 1;
            *(undefined1 *)(local_8 + 0x67) = 0;
            *(undefined1 *)(local_8 + 0x7f) = 0;
            break;
          case 0x308b:
            *(undefined1 *)(local_8 + 0x47) = 3;
            *(undefined1 *)(local_8 + 0x5f) = 0;
            *(undefined1 *)(local_8 + 0x77) = 0xff;
            break;
          case 0x3095:
            *(undefined1 *)(local_8 + 0x3e) = 3;
            *(undefined1 *)(local_8 + 0x56) = 0;
            *(undefined1 *)(local_8 + 0x6e) = 0xff;
            *(undefined1 *)(local_8 + 0x45) = 3;
            *(undefined1 *)(local_8 + 0x5d) = 0;
            *(undefined1 *)(local_8 + 0x75) = 0xff;
            break;
          case 0x3099:
            *(undefined1 *)(local_8 + 0x3f) = 3;
            *(undefined1 *)(local_8 + 0x57) = 0;
            *(undefined1 *)(local_8 + 0x6f) = 0xff;
            break;
          case 0x309d:
            *(undefined1 *)(local_8 + 0x46) = 3;
            *(undefined1 *)(local_8 + 0x5e) = 0;
            *(undefined1 *)(local_8 + 0x76) = 0xff;
            *(undefined1 *)(local_8 + 0x4b) = 3;
            *(undefined1 *)(local_8 + 99) = 0;
            *(undefined1 *)(local_8 + 0x7b) = 0xff;
            break;
          case 0x30ab:
            *(undefined1 *)(local_8 + 0x41) = 3;
            *(undefined1 *)(local_8 + 0x59) = 0;
            *(undefined1 *)(local_8 + 0x71) = 0xff;
          }
        }
      }
      else {
        local_6c = local_10 + -0x30b5;
        switch(local_10) {
        case 0x30b5:
          *(undefined1 *)(local_8 + 0x40) = 3;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined1 *)(local_8 + 0x70) = 0xff;
          *(undefined1 *)(local_8 + 0x43) = 3;
          *(undefined1 *)(local_8 + 0x5b) = 0;
          *(undefined1 *)(local_8 + 0x73) = 0xff;
          break;
        case 0x30b9:
          *(undefined1 *)(local_8 + 0x12a) = 1;
          *(undefined2 *)(local_8 + 0x12e) = 0;
          *(undefined1 *)(local_8 + 300) = 0;
          break;
        case 0x30bb:
          *(undefined1 *)(local_8 + 0x42) = 3;
          *(undefined1 *)(local_8 + 0x5a) = 0;
          *(undefined1 *)(local_8 + 0x72) = 0xff;
          *(undefined1 *)(local_8 + 0x49) = 3;
          *(undefined1 *)(local_8 + 0x61) = 0;
          *(undefined1 *)(local_8 + 0x79) = 0xff;
          *(undefined1 *)(local_8 + 0x4c) = 3;
          *(undefined1 *)(local_8 + 100) = 0;
          *(undefined1 *)(local_8 + 0x7c) = 0xff;
          break;
        case 0x30bf:
          *(undefined1 *)(local_8 + 0x39) = 3;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0xff;
          *(undefined1 *)(local_8 + 0x3c) = 3;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0xff;
          *(undefined1 *)(local_8 + 0x4d) = 3;
          *(undefined1 *)(local_8 + 0x65) = 0;
          *(undefined1 *)(local_8 + 0x7d) = 0xff;
          *(undefined1 *)(local_8 + 0x4f) = 3;
          *(undefined1 *)(local_8 + 0x67) = 0;
          *(undefined1 *)(local_8 + 0x7f) = 0xff;
          break;
        case 0x30c1:
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
          *(undefined1 *)(local_8 + 0x48) = 3;
          *(undefined1 *)(local_8 + 0x60) = 0;
          *(undefined1 *)(local_8 + 0x78) = 0xff;
          break;
        case 0x30c3:
          *(undefined1 *)(local_8 + 0x4e) = 3;
          *(undefined1 *)(local_8 + 0x66) = 0;
          *(undefined1 *)(local_8 + 0x7e) = 0xff;
          break;
        case 0x30c5:
          *(undefined1 *)(local_8 + 0x3d) = 3;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0xff;
          break;
        case 0x30c9:
          *(undefined1 *)(local_8 + 0x3b) = 3;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0xff;
          break;
        case 0x30d3:
          *(undefined1 *)(local_8 + 0x44) = 3;
          *(undefined1 *)(local_8 + 0x5c) = 0;
          *(undefined1 *)(local_8 + 0x74) = 0xff;
          break;
        case 0x30e1:
          *(undefined1 *)(local_8 + 0x50) = 1;
          *(undefined1 *)(local_8 + 0x68) = 0;
          *(undefined1 *)(local_8 + 0x80) = 0;
          break;
        case 0x313f:
          *(undefined1 *)(local_8 + 0x50) = 3;
          *(undefined1 *)(local_8 + 0x68) = 0;
          *(undefined1 *)(local_8 + 0x80) = 0xff;
        }
      }
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__0050d5a0();
      FUN__text__00515040();
      FUN__text__0051b9c0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0050afd0();
        FUN__text__0050b900();
        FUN__text__00513480();
        FUN__text__00514170();
        FUN__text__0051afe0();
        FUN__text__0051b380();
        iVar1 = local_10;
      }
      break;
    case 0x11:
      if (iVar1 < 0x328b) {
        if (iVar1 == 0x328a) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
        else if (iVar1 == 0x3184) {
          *(undefined1 *)(local_8 + 0x34) = 0xd;
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0;
        }
        else if (iVar1 == 0x3252) {
          *(undefined1 *)(local_8 + 0x39) = 3;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0xff;
        }
      }
      else if (iVar1 == 0x3364) {
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
      }
      local_70 = iVar1;
      local_10 = iVar1;
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0x12:
      local_74 = iVar1;
      if (iVar1 < 0x33cf) {
        if (iVar1 == 0x33ce) {
          *(undefined1 *)(local_8 + 0x43) = 1;
          *(undefined1 *)(local_8 + 0x5b) = 0;
          *(undefined1 *)(local_8 + 0x73) = 0;
        }
        else {
          local_74 = local_10 + -0x33af;
          switch(local_10) {
          case 0x33af:
            *(undefined1 *)(local_8 + 0x34) = 0xe;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            break;
          case 0x33b5:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            break;
          case 0x33b7:
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
            break;
          case 0x33bf:
            *(undefined1 *)(local_8 + 0x3c) = 1;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0;
            break;
          case 0x33c5:
            *(undefined1 *)(local_8 + 0x3d) = 1;
            *(undefined1 *)(local_8 + 0x55) = 0;
            *(undefined1 *)(local_8 + 0x6d) = 0;
            *(undefined1 *)(local_8 + 0x3e) = 1;
            *(undefined1 *)(local_8 + 0x56) = 0;
            *(undefined1 *)(local_8 + 0x6e) = 0;
            break;
          case 0x33c7:
            *(undefined1 *)(local_8 + 0x3f) = 1;
            *(undefined1 *)(local_8 + 0x57) = 0;
            *(undefined1 *)(local_8 + 0x6f) = 0;
            break;
          case 0x33c9:
            *(undefined1 *)(local_8 + 0x40) = 1;
            *(undefined1 *)(local_8 + 0x58) = 0;
            *(undefined1 *)(local_8 + 0x70) = 0;
            *(undefined1 *)(local_8 + 0x41) = 1;
            *(undefined1 *)(local_8 + 0x59) = 0;
            *(undefined1 *)(local_8 + 0x71) = 0;
            *(undefined1 *)(local_8 + 0x42) = 1;
            *(undefined1 *)(local_8 + 0x5a) = 0;
            *(undefined1 *)(local_8 + 0x72) = 0;
          }
        }
      }
      else if (iVar1 < 0x3485) {
        if (iVar1 == 0x3484) {
          *(undefined1 *)(local_8 + 0x47) = 1;
          *(undefined1 *)(local_8 + 0x5f) = 0;
          *(undefined1 *)(local_8 + 0x77) = 0;
        }
        else if (iVar1 == 0x33d2) {
          *(undefined1 *)(local_8 + 0x44) = 1;
          *(undefined1 *)(local_8 + 0x5c) = 0;
          *(undefined1 *)(local_8 + 0x74) = 0;
        }
        else if (iVar1 == 0x33d8) {
          *(undefined1 *)(local_8 + 0x45) = 1;
          *(undefined1 *)(local_8 + 0x5d) = 0;
          *(undefined1 *)(local_8 + 0x75) = 0;
        }
        else if (iVar1 == 0x33dc) {
          *(undefined1 *)(local_8 + 0x46) = 1;
          *(undefined1 *)(local_8 + 0x5e) = 0;
          *(undefined1 *)(local_8 + 0x76) = 0;
        }
      }
      else if (iVar1 == 0x3532) {
        *(undefined1 *)(local_8 + 0x47) = 3;
        *(undefined1 *)(local_8 + 0x5f) = 0;
        *(undefined1 *)(local_8 + 0x77) = 0xff;
      }
      else if (iVar1 == 0x3564) {
        *(undefined1 *)(local_8 + 0x48) = 1;
        *(undefined1 *)(local_8 + 0x60) = 0;
        *(undefined1 *)(local_8 + 0x78) = 0;
      }
      else if (iVar1 == 0x3624) {
        *(undefined1 *)(local_8 + 0x48) = 3;
        *(undefined1 *)(local_8 + 0x60) = 0;
        *(undefined1 *)(local_8 + 0x78) = 0xff;
      }
      local_10 = iVar1;
      FUN__text__0050d5a0();
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0050b900();
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0x13:
      if (iVar1 < 0x3785) {
        if (iVar1 == 0x3784) {
          *(undefined1 *)(local_8 + 0x39) = 3;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0xff;
        }
        else if (iVar1 == 0x366c) {
          *(undefined1 *)(local_8 + 0x35) = 0xb;
          *(undefined1 *)(local_8 + 0xea) = 1;
          *(undefined2 *)(local_8 + 0xf2) = 0;
          *(undefined2 *)(local_8 + 0x11a) = DAT_00757d6e;
          *(undefined1 *)(local_8 + 0xeb) = 2;
          *(undefined2 *)(local_8 + 0xf4) = 0;
          *(undefined1 *)(local_8 + 0x103) = 0xff;
          *(undefined2 *)(local_8 + 0x11c) = DAT_00757d7e;
          *(undefined1 *)(local_8 + 0x37) = 7;
          *(undefined1 *)(local_8 + 0x12a) = 3;
          *(undefined2 *)(local_8 + 0x12e) = 0;
          *(undefined1 *)(local_8 + 300) = 0xff;
        }
        else if (iVar1 == 0x369c) {
          *(undefined1 *)(local_8 + 0x34) = 0xf;
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0;
        }
        else if (iVar1 == 0x36ec) {
          *(undefined1 *)(local_8 + 0xec) = 1;
          *(undefined2 *)(local_8 + 0xf6) = 0;
          *(undefined1 *)(local_8 + 0x104) = 0;
          *(undefined2 *)(local_8 + 0x11e) = DAT_00757d8e;
        }
      }
      else if (iVar1 == 0x37be) {
        *(undefined1 *)(local_8 + 0x12a) = 1;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0;
      }
      else if (iVar1 == 0x380e) {
        *(undefined1 *)(local_8 + 0x3a) = 1;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0;
      }
      else if (iVar1 == 0x391e) {
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
      }
      local_78 = iVar1;
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__00515040();
      FUN__text__0051b9c0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051c6c0();
        FUN__text__0051ca00();
        FUN__text__0051d1d0();
        FUN__text__00513480();
        FUN__text__00514170();
        FUN__text__0051afe0();
        FUN__text__0051b380();
        iVar1 = local_10;
      }
      break;
    case 0x14:
      local_7c = iVar1;
      if (iVar1 < 0x3a5d) {
        if (iVar1 == 0x3a5c) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
        else {
          local_7c = local_10 + -0x396d;
          switch(local_10) {
          case 0x396d:
            *(undefined1 *)(local_8 + 0x34) = 0x10;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            break;
          case 0x3981:
            *(undefined1 *)(local_8 + 0x35) = 0xc;
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined2 *)(local_8 + 0x11a) = DAT_00757d9e;
            *(undefined1 *)(local_8 + 0x37) = 8;
            *(undefined1 *)(local_8 + 0x12a) = 3;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0xff;
            break;
          case 0x39b5:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            break;
          case 0x3a4b:
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
          }
        }
      }
      else if (iVar1 < 0x3c25) {
        if (iVar1 == 0x3c24) {
          *(undefined1 *)(local_8 + 0x3c) = 2;
          *(undefined1 *)(local_8 + 299) = 3;
          *(undefined2 *)(local_8 + 0x130) = 0;
          *(undefined1 *)(local_8 + 0x12d) = 0xff;
        }
        else if (iVar1 == 15000) {
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
        }
        else if (iVar1 == 0x3ba0) {
          *(undefined1 *)(local_8 + 299) = 1;
          *(undefined2 *)(local_8 + 0x130) = 0;
          *(undefined1 *)(local_8 + 0x12d) = 0;
        }
      }
      else if (iVar1 == 0x3ce8) {
        *(undefined1 *)(local_8 + 0x3c) = 3;
        *(undefined1 *)(local_8 + 0x54) = 0;
        *(undefined1 *)(local_8 + 0x6c) = 0xff;
      }
      local_10 = iVar1;
      FUN__text__0051e2b0();
      FUN__text__00515040();
      FUN__text__0051b9c0();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__0051d1d0();
        FUN__text__00513480();
        FUN__text__00514170();
        FUN__text__0051afe0();
        FUN__text__0051b380();
        iVar1 = local_10;
      }
      break;
    case 0x15:
      if (iVar1 == 0x3d56) {
        *(undefined1 *)(local_8 + 0x34) = 0x11;
        *(undefined1 *)(local_8 + 0x39) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
      }
      else if (iVar1 == 0x3ed4) {
        *(undefined1 *)(local_8 + 0x39) = 3;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0xff;
      }
      local_80 = iVar1;
      local_10 = iVar1;
      FUN__text__00515040();
      iVar1 = local_10;
      if (local_14 == 0) {
        FUN__text__00513480();
        FUN__text__00514170();
        iVar1 = local_10;
      }
      break;
    case 0x16:
      local_84 = iVar1;
      if (iVar1 == 0x3f4c) {
        *(undefined1 *)(local_8 + 0x30) = 100;
      }
      break;
    case 100:
      local_10 = iVar1;
      goto LAB__text__0050a04d;
    }
    local_10 = iVar1;
    FUN__text__00422360(0);
  } while ((*(uint *)(DAT_007a49fc + 0x1990) & 1) == 0);
LAB__text__0050a04d:
  FUN__text__004db230(0x3c);
  while (iVar1 = FUN__text__004db270(), iVar1 == 0) {
    FUN__text__00422360(0);
  }
  FUN__text__00422360(0);
  FUN__text__00422360(0);
  FUN__text__0041e500();
  FUN__text__0041f4e0(10);
  FUN__text__00415480(1,10);
  FUN__text__00415420();
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    FUN__text__00464d30();
  }
  FUN__text__00439e30(1);
  local_8 = 0x50a119;
  FUN__text__0056ce80();
  return;
}

