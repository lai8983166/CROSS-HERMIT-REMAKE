
void FUN__text__004e3ae0(void)

{
  byte bVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_c0 [16];
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
  uint local_38;
  char local_34;
  uint local_30;
  uint local_2c;
  char local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_c0;
  for (iVar2 = 0x2f; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__00415480(1,0x3c);
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__004e77b0();
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__00416a10(local_8 + 0x1e0);
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__00415420();
LAB__text__004e3b78:
  local_10 = 0;
  local_14 = 0;
  local_18 = 0;
  local_1c = 0;
  local_20 = 0;
  local_24 = 0;
  local_28 = '\0';
  FUN__text__00505df0();
  FUN__text__004faaa0();
  FUN__text__00409ef0(local_8 + 0x5a8);
  FUN__text__00409ff0(local_8 + 0x5a8,0,2,0x80);
  FUN__text__00415420();
  FUN__text__004db060(0x1f,0);
  while (iVar2 = FUN__text__0041e3d0(), iVar2 == 0) {
    FUN__text__00422360(0);
  }
  FUN__text__00415420();
  do {
    if (*(byte *)(local_8 + 0x32) < 0xe) {
      if (*(byte *)(local_8 + 0x32) < 4) {
        for (local_c = 0; local_c < 2; local_c = local_c + 1) {
          FUN__text__00410310(*(undefined2 *)(&DAT_00753204 + local_c * 10),
                              *(undefined2 *)(&DAT_00753206 + local_c * 10),
                              *(undefined2 *)(&DAT_00753208 + local_c * 10),
                              *(undefined2 *)(&DAT_0075320a + local_c * 10),
                              *(undefined2 *)(&DAT_0075320c + local_c * 10),0xff000000,0);
        }
      }
      else {
        for (local_c = 2; local_c < 4; local_c = local_c + 1) {
          FUN__text__00410310(*(undefined2 *)(&DAT_00753204 + local_c * 10),
                              *(undefined2 *)(&DAT_00753206 + local_c * 10),
                              *(undefined2 *)(&DAT_00753208 + local_c * 10),
                              *(undefined2 *)(&DAT_0075320a + local_c * 10),
                              *(undefined2 *)(&DAT_0075320c + local_c * 10),0xff000000,0);
        }
      }
    }
    local_34 = local_28;
    if (local_28 == '\x01') {
      if (local_14 == 0) {
        local_2c = CONCAT31(local_2c._1_3_,(&DAT_00755d00)[local_30 & 0xff]);
        bVar1 = (char)local_30 + 1;
        local_30 = CONCAT31(local_30._1_3_,bVar1);
        if (0x16 < bVar1) {
          local_30 = (uint)local_30._1_3_ << 8;
          local_28 = '\x02';
        }
      }
      for (local_c = 0xa7; local_c < 0xaa; local_c = local_c + 1) {
        FUN__text__00505580((int)*(short *)(&DAT_00752724 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752726 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752728 + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272a + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272c + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272e + local_c * 0x10),
                            (int)*(short *)(&DAT_00752730 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752732 + local_c * 0x10),local_2c & 0xff,0x80,
                            0x80,0x80);
      }
    }
    else if (local_28 == '\x02') {
      for (local_c = 0xa7; local_c < 0xaa; local_c = local_c + 1) {
        FUN__text__00505000((int)*(short *)(&DAT_00752724 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752726 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752728 + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272a + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272c + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272e + local_c * 0x10),
                            (int)*(short *)(&DAT_00752730 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752732 + local_c * 0x10));
      }
    }
    else if (local_28 == '\x03') {
      if (local_14 == 0) {
        local_2c = CONCAT31(local_2c._1_3_,(&DAT_00756c6c)[local_30 & 0xff]);
        bVar1 = (char)local_30 + 1;
        local_30 = CONCAT31(local_30._1_3_,bVar1);
        if (0x18 < bVar1) {
          local_30 = (uint)local_30._1_3_ << 8;
          local_28 = '\0';
        }
      }
      for (local_c = 0xa7; local_c < 0xaa; local_c = local_c + 1) {
        FUN__text__00505580((int)*(short *)(&DAT_00752724 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752726 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752728 + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272a + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272c + local_c * 0x10),
                            (int)*(short *)(&DAT_0075272e + local_c * 0x10),
                            (int)*(short *)(&DAT_00752730 + local_c * 0x10),
                            (int)*(short *)(&DAT_00752732 + local_c * 0x10),local_2c & 0xff,0x80,
                            0x80,0x80);
      }
    }
    iVar2 = local_10 + 1;
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
    local_38 = (uint)*(byte *)(local_8 + 0x32);
    switch(local_38) {
    case 0:
      local_3c = local_10 + -0x1d;
      switch(local_10) {
      case 0x1d:
        *(undefined1 *)(local_8 + 0x39) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
        local_28 = '\x01';
        local_2c = (uint)local_2c._1_3_ << 8;
        local_30 = (uint)local_30._1_3_ << 8;
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
      local_10 = iVar2;
      FUN__text__004fa1f0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004fa0e0();
        FUN__text__004f9fc0();
        iVar2 = local_10;
      }
      break;
    case 1:
      local_40 = iVar2;
      if (iVar2 < 0x9b5) {
        if (iVar2 == 0x9b4) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
        else if (iVar2 < 0x501) {
          if (iVar2 == 0x500) {
            *(undefined1 *)(local_8 + 0x3a) = 3;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0xff;
          }
          else if (iVar2 < 0x2ef) {
            if (iVar2 == 0x2ee) {
              *(undefined1 *)(local_8 + 0x3b) = 1;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0;
            }
            else if (iVar2 < 0x19b) {
              if (iVar2 == 0x19a) {
                *(undefined1 *)(local_8 + 0x39) = 3;
                *(undefined1 *)(local_8 + 0x51) = 0;
                *(undefined1 *)(local_8 + 0x69) = 0xff;
              }
              else if (iVar2 == 0x136) {
                *(undefined1 *)(local_8 + 0x33) = 1;
                *(undefined1 *)(local_8 + 0x39) = 1;
                *(undefined1 *)(local_8 + 0x51) = 0;
                *(undefined1 *)(local_8 + 0x69) = 0;
              }
              else if (iVar2 == 0x154) {
                *(undefined1 *)(local_8 + 0x35) = 1;
                *(undefined1 *)(local_8 + 0xea) = 1;
                *(undefined2 *)(local_8 + 0xf2) = 0;
                *(undefined2 *)(local_8 + 0x11a) = DAT_0075230a;
              }
            }
            else if (iVar2 == 0x1ae) {
              *(undefined1 *)(local_8 + 0x3a) = 1;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0;
            }
            else if (iVar2 == 0x2da) {
              *(undefined1 *)(local_8 + 0x3a) = 3;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0xff;
            }
          }
          else {
            local_40 = local_10 + -0x397;
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
        else if (iVar2 < 0x6eb) {
          if (iVar2 == 0x6ea) {
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
          }
          else if (iVar2 < 0x62d) {
            if (iVar2 == 0x62c) {
              *(undefined1 *)(local_8 + 0x3a) = 1;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0;
            }
            else if (iVar2 == 0x532) {
              *(undefined1 *)(local_8 + 0x33) = 3;
              *(undefined1 *)(local_8 + 0x39) = 1;
              *(undefined1 *)(local_8 + 0x51) = 0;
              *(undefined1 *)(local_8 + 0x69) = 0;
            }
            else if (iVar2 == 0x618) {
              *(undefined1 *)(local_8 + 0x39) = 3;
              *(undefined1 *)(local_8 + 0x51) = 0;
              *(undefined1 *)(local_8 + 0x69) = 0xff;
            }
          }
          else if (iVar2 == 0x6d6) {
            *(undefined1 *)(local_8 + 0x3a) = 3;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0xff;
          }
        }
        else if (iVar2 < 0x91b) {
          if (iVar2 == 0x91a) {
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
          }
          else if (iVar2 == 0x7e4) {
            *(undefined1 *)(local_8 + 0x3b) = 3;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0xff;
          }
          else if (iVar2 == 0x816) {
            *(undefined1 *)(local_8 + 0x33) = 4;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
        }
        else if (iVar2 == 0x92e) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
      }
      else if (iVar2 < 0xe2f) {
        if (iVar2 == 0xe2e) {
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
        }
        else if (iVar2 < 0xc27) {
          if (iVar2 == 0xc26) {
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
          }
          else if (iVar2 < 0xa83) {
            if (iVar2 == 0xa82) {
              *(undefined1 *)(local_8 + 0x3c) = 1;
              *(undefined1 *)(local_8 + 0x54) = 0;
              *(undefined1 *)(local_8 + 0x6c) = 0;
            }
            else if (iVar2 == 0x9ce) {
              *(undefined1 *)(local_8 + 0x3b) = 1;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0;
            }
            else if (iVar2 == 0xa6e) {
              *(undefined1 *)(local_8 + 0x3b) = 3;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0xff;
            }
          }
          else if (iVar2 == 0xb2c) {
            *(undefined1 *)(local_8 + 0x3c) = 3;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0xff;
          }
          else if (iVar2 == 0xb5e) {
            *(undefined1 *)(local_8 + 0x33) = 5;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
        }
        else if (iVar2 < 0xcf9) {
          if (iVar2 == 0xcf8) {
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
          }
          else if (iVar2 == 0xc58) {
            *(undefined1 *)(local_8 + 0x33) = 6;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
          else if (iVar2 == 0xce4) {
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
          }
        }
        else if (iVar2 == 0xe1a) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
      }
      else if (iVar2 < 0x1091) {
        if (iVar2 == 0x1090) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
        else {
          local_40 = local_10 + -0xf09;
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
        local_40 = local_10 + -0x10a3;
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
      local_10 = iVar2;
      FUN__text__004f7f20();
      FUN__text__004f4d00();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f7890();
        FUN__text__004f71c0();
        FUN__text__004f3ae0();
        FUN__text__004f3810();
        FUN__text__004f4200();
        iVar2 = local_10;
      }
      break;
    case 2:
      if (iVar2 < 0x1331) {
        local_44 = iVar2;
        if (iVar2 == 0x1330) {
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined2 *)(local_8 + 0x82) = DAT_00752898;
          *(undefined2 *)(local_8 + 0x9c) = DAT_0075289a;
        }
        else if (iVar2 < 0x1287) {
          if (iVar2 == 0x1286) {
            *(undefined1 *)(local_8 + 0xed) = 1;
            *(undefined2 *)(local_8 + 0xf8) = 0;
            *(undefined2 *)(local_8 + 0x120) = DAT_007523ea;
          }
          else if (iVar2 == 0x11f0) {
            *(undefined1 *)(local_8 + 0x38) = 1;
            *(undefined1 *)(local_8 + 0x142) = 1;
            *(undefined2 *)(local_8 + 0x144) = 0;
            *(undefined2 *)(local_8 + 0x14c) = 0;
          }
          else if (iVar2 == 0x1254) {
            *(undefined1 *)(local_8 + 0xeb) = 1;
            *(undefined2 *)(local_8 + 0xf4) = 0;
            *(undefined2 *)(local_8 + 0x11c) = DAT_0075231a;
          }
          else if (iVar2 == 0x1284) {
            *(undefined1 *)(local_8 + 0xec) = 1;
            *(undefined2 *)(local_8 + 0xf6) = 0;
            *(undefined2 *)(local_8 + 0x11e) = DAT_0075239a;
          }
        }
        else if (iVar2 == 0x12d2) {
          *(undefined1 *)(local_8 + 0xee) = 1;
          *(undefined2 *)(local_8 + 0xfa) = 0;
          *(undefined2 *)(local_8 + 0x122) = DAT_007523fa;
        }
        else if (iVar2 == 0x1302) {
          *(undefined1 *)(local_8 + 0xef) = 1;
          *(undefined2 *)(local_8 + 0xfc) = 0;
          *(undefined2 *)(local_8 + 0x124) = DAT_0075240a;
        }
        else if (iVar2 == 0x1320) {
          *(undefined1 *)(local_8 + 0x37) = 1;
          *(undefined1 *)(local_8 + 0x12a) = 1;
          *(undefined2 *)(local_8 + 0x12e) = 0;
          *(undefined1 *)(local_8 + 300) = 0;
        }
      }
      else {
        local_44 = local_10 + -0x1333;
        switch(local_10) {
        case 0x1333:
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined2 *)(local_8 + 0x84) = DAT_007528a8;
          *(undefined2 *)(local_8 + 0x9e) = DAT_007528aa;
          break;
        case 0x1335:
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined2 *)(local_8 + 0x86) = DAT_007528b8;
          *(undefined2 *)(local_8 + 0xa0) = PTR_DAT_007528ba._0_2_;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined2 *)(local_8 + 0x88) = DAT_007528c8;
          *(undefined2 *)(local_8 + 0xa2) = DAT_007528ca;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined2 *)(local_8 + 0x8a) = DAT_007528d8;
          *(undefined2 *)(local_8 + 0xa4) = DAT_007528da;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_007528e8;
          *(undefined2 *)(local_8 + 0xa6) = DAT_007528ea;
          break;
        case 0x1337:
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined2 *)(local_8 + 0x8e) = DAT_007528f8;
          *(undefined2 *)(local_8 + 0xa8) = DAT_007528fa;
          break;
        case 0x1339:
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined2 *)(local_8 + 0x90) = DAT_00752908;
          *(undefined2 *)(local_8 + 0xaa) = DAT_0075290a;
          *(undefined1 *)(local_8 + 0x59) = 0;
          *(undefined2 *)(local_8 + 0x92) = DAT_00752918;
          *(undefined2 *)(local_8 + 0xac) = DAT_0075291a;
          break;
        case 0x133b:
          *(undefined1 *)(local_8 + 0x42) = 1;
          *(undefined1 *)(local_8 + 0x5a) = 0;
          *(undefined2 *)(local_8 + 0x94) = DAT_00752928;
          *(undefined2 *)(local_8 + 0xae) = DAT_0075292a;
          break;
        case 0x133d:
          *(undefined1 *)(local_8 + 0x43) = 1;
          *(undefined1 *)(local_8 + 0x5b) = 0;
          *(undefined2 *)(local_8 + 0x96) = DAT_00752938;
          *(undefined2 *)(local_8 + 0xb0) = DAT_0075293a;
          *(undefined2 *)(local_8 + 0xca) = 0x153;
          *(undefined2 *)(local_8 + 0xe4) = 0x1a;
          *(undefined1 *)(local_8 + 0x44) = 1;
          *(undefined1 *)(local_8 + 0x5c) = 0;
          *(undefined2 *)(local_8 + 0x98) = DAT_00752418;
          *(undefined2 *)(local_8 + 0xb2) = DAT_0075241a;
          *(undefined2 *)(local_8 + 0xcc) = 0x200;
          *(undefined2 *)(local_8 + 0xe6) = 0x180;
          break;
        case 0x1347:
          *(undefined1 *)(local_8 + 0x45) = 1;
          *(undefined1 *)(local_8 + 0x5d) = 0;
          *(undefined2 *)(local_8 + 0x9a) = DAT_00752428;
          *(undefined2 *)(local_8 + 0xce) = 300;
          *(undefined2 *)(local_8 + 0xe8) = 300;
        }
      }
      local_10 = iVar2;
      FUN__text__004fa960();
      FUN__text__004f4d00();
      FUN__text__004f1dc0();
      FUN__text__004f2dc0();
      if (local_14 == 0) {
        FUN__text__004f3ae0();
        FUN__text__004f3810();
        FUN__text__004f4200();
        FUN__text__004fa6f0();
      }
      if (local_18 == 0) {
        FUN__text__004f2880();
      }
      iVar2 = local_10;
      if (local_24 == 0) {
        FUN__text__004f1710();
        iVar2 = local_10;
      }
      break;
    case 3:
      if (iVar2 == 0x13b6) {
        *(undefined1 *)(local_8 + 0x36) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
        *(undefined2 *)(local_8 + 0xb6) = 0x24e;
        *(undefined2 *)(local_8 + 0xd0) = 0x1bb;
      }
      local_48 = iVar2;
      local_10 = iVar2;
      FUN__text__004f1510();
      iVar2 = local_10;
      if (local_18 == 0) {
        FUN__text__004f13f0();
        FUN__text__004f13a0();
        FUN__text__004f1440();
        iVar2 = local_10;
      }
      break;
    case 4:
      if (iVar2 < 0x161f) {
        local_4c = iVar2;
        if (iVar2 == 0x161e) {
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined2 *)(local_8 + 0x8e) = PTR_DAT_00752fa8._0_2_;
        }
        else if (iVar2 < 0x15db) {
          if (iVar2 == 0x15da) {
            *(undefined1 *)(local_8 + 0x12a) = 3;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0xff;
            *(undefined1 *)(local_8 + 0x39) = 3;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0xff;
            *(undefined1 *)(local_8 + 0xeb) = 1;
            *(undefined1 *)(local_8 + 0xec) = 1;
            *(undefined2 *)(local_8 + 0xf6) = 0;
            *(undefined2 *)(local_8 + 0x10e) = DAT_007524e8;
            *(undefined1 *)(local_8 + 0xed) = 1;
            *(undefined2 *)(local_8 + 0xf8) = 0;
            *(undefined2 *)(local_8 + 0x110) = DAT_00752468;
            *(undefined2 *)(local_8 + 0x120) = DAT_0075246a;
            *(undefined1 *)(local_8 + 0xee) = 1;
            *(undefined2 *)(local_8 + 0xfa) = 0;
            *(undefined2 *)(local_8 + 0x112) = DAT_00752488;
            *(undefined2 *)(local_8 + 0x122) = DAT_0075248a;
            *(undefined1 *)(local_8 + 0xef) = 1;
            *(undefined2 *)(local_8 + 0xfc) = 0;
            *(undefined2 *)(local_8 + 0x114) = DAT_007524a8;
            *(undefined2 *)(local_8 + 0x124) = DAT_007524aa;
            *(undefined1 *)(local_8 + 0xf0) = 1;
            *(undefined2 *)(local_8 + 0xfe) = 0;
            *(undefined2 *)(local_8 + 0x116) = DAT_007524c8;
            *(undefined2 *)(local_8 + 0x126) = DAT_007524ca;
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined2 *)(local_8 + 0xa0) = 0x115;
            *(undefined1 *)(local_8 + 0x3c) = 1;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined2 *)(local_8 + 0x88) = DAT_00752f78;
            *(undefined2 *)(local_8 + 0xa2) = DAT_00752f7a;
          }
          else if (iVar2 == 0x14f0) {
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined2 *)(local_8 + 0x11a) = DAT_0075243a;
            *(undefined1 *)(local_8 + 0x102) = 0;
          }
          else if (iVar2 == 0x157d) {
            *(undefined1 *)(local_8 + 0x37) = 2;
            *(undefined1 *)(local_8 + 0x12a) = 1;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0;
          }
          else if (iVar2 == 0x1589) {
            *(undefined1 *)(local_8 + 0x34) = 1;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
        }
        else if (iVar2 == 0x1606) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined2 *)(local_8 + 0x8a) = PTR_DAT_00752f98._0_2_;
        }
        else if (iVar2 == 0x1616) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_00752f88;
          *(undefined2 *)(local_8 + 0xa6) = DAT_00752f8a;
        }
      }
      else {
        local_4c = local_10 + -0x1651;
        switch(local_10) {
        case 0x1651:
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined2 *)(local_8 + 0x8c) = DAT_00752f88;
          *(undefined2 *)(local_8 + 0xa6) = DAT_00752f8a;
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined2 *)(local_8 + 0x8e) = PTR_DAT_00752fa8._0_2_;
          break;
        case 0x1656:
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined2 *)(local_8 + 0x88) = DAT_00752f78;
          *(undefined2 *)(local_8 + 0xa2) = DAT_00752f7a;
          break;
        case 0x1686:
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined2 *)(local_8 + 0x8a) = PTR_DAT_00752f98._0_2_;
          break;
        case 0x168b:
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined2 *)(local_8 + 0x88) = DAT_00752f78;
          *(undefined2 *)(local_8 + 0xa2) = DAT_00752f7a;
          break;
        case 0x1694:
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined2 *)(local_8 + 0x90) = PTR_DAT_00752f98._0_2_;
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
      local_10 = iVar2;
      FUN__text__004f1080();
      FUN__text__004f2dc0();
      FUN__text__004ee6b0();
      FUN__text__004ecab0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f0f70();
        FUN__text__004f0fc0();
        FUN__text__004f2880();
        FUN__text__004f2640();
        FUN__text__004edec0();
        FUN__text__004ed6f0();
        FUN__text__004ec540();
        iVar2 = local_10;
      }
      break;
    case 5:
      if (iVar2 == 0x1718) {
        *(undefined1 *)(local_8 + 0x41) = 3;
        *(undefined1 *)(local_8 + 0x59) = 0;
        *(undefined1 *)(local_8 + 0x71) = 0xff;
      }
      else if (iVar2 == 0x1742) {
        *(undefined1 *)(local_8 + 0x35) = 2;
        *(undefined1 *)(local_8 + 0xea) = 1;
        *(undefined2 *)(local_8 + 0xf2) = 0;
        *(undefined1 *)(local_8 + 0x102) = 0;
      }
      local_50 = iVar2;
      local_10 = iVar2;
      FUN__text__004ee6b0();
      FUN__text__004f4d00();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004ed6f0();
        FUN__text__004f3ae0();
        iVar2 = local_10;
      }
      break;
    case 6:
      if (iVar2 < 0x17fc) {
        if (iVar2 == 0x17fb) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
          local_54 = 0x17fb;
        }
        else {
          local_54 = local_10 + -0x1756;
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
        local_54 = local_10 + -0x1812;
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
          *(undefined2 *)(local_8 + 0x134) = DAT_0075325e;
          *(undefined2 *)(local_8 + 0x13a) = DAT_00753258;
          *(undefined2 *)(local_8 + 0x13c) = DAT_00753262;
        }
      }
      local_10 = iVar2;
      FUN__text__004f4d00();
      FUN__text__004e8f10();
      FUN__text__004ee6b0();
      FUN__text__004f2dc0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f3ae0();
        FUN__text__004e7ad0();
        FUN__text__004edec0();
        FUN__text__004ed6f0();
        FUN__text__004f2880();
        FUN__text__004f2cb0();
        iVar2 = local_10;
      }
      break;
    case 7:
      if (iVar2 < 0x1a13) {
        if (iVar2 == 0x1a12) {
          *(undefined1 *)(local_8 + 0xeb) = 1;
          *(undefined2 *)(local_8 + 0xf4) = 0;
          *(undefined1 *)(local_8 + 0x103) = 0;
          *(undefined2 *)(local_8 + 0x10c) = PTR_DAT_00752598._0_2_;
        }
        else if (iVar2 < 0x1939) {
          if (iVar2 == 0x1938) {
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
          }
          else if (iVar2 == 0x18a8) {
            *(undefined1 *)(local_8 + 0x35) = 3;
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined1 *)(local_8 + 0x102) = 0;
            *(undefined2 *)(local_8 + 0x10a) = PTR_DAT_00752588._0_2_;
          }
          else if (iVar2 == 0x18e5) {
            *(undefined1 *)(local_8 + 0x34) = 3;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            *(undefined2 *)(local_8 + 0x82) = DAT_00752df8;
            *(undefined2 *)(local_8 + 0x9c) = DAT_00752dfa;
          }
          else if (iVar2 == 0x18f6) {
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            *(undefined2 *)(local_8 + 0x84) = DAT_00752e98;
            *(undefined2 *)(local_8 + 0x9e) = DAT_00752e9a;
          }
        }
        else if (iVar2 == 0x196b) {
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0;
        }
        else if (iVar2 == 0x19e5) {
          *(undefined1 *)(local_8 + 0x3b) = 3;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0xff;
        }
        else if (iVar2 == 0x19ec) {
          *(undefined1 *)(local_8 + 0x3c) = 3;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0xff;
        }
      }
      else if (iVar2 < 0x1b79) {
        if (iVar2 == 0x1b78) {
          *(undefined1 *)(local_8 + 0x3e) = 3;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0xff;
        }
        else if (iVar2 == 0x1a42) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
        }
        else if (iVar2 == 0x1a9f) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
        }
        else if (iVar2 == 0x1b6f) {
          *(undefined1 *)(local_8 + 0x3d) = 3;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0xff;
        }
      }
      else if (iVar2 == 0x1b7e) {
        *(undefined1 *)(local_8 + 0x12a) = 3;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0xff;
      }
      else if (iVar2 == 0x1bb8) {
        *(undefined1 *)(local_8 + 0x3f) = 1;
        *(undefined1 *)(local_8 + 0x57) = 0;
        *(undefined1 *)(local_8 + 0x6f) = 0;
      }
      local_58 = iVar2;
      local_10 = iVar2;
      FUN__text__004f2dc0();
      FUN__text__004f4d00();
      FUN__text__004e8f10();
      FUN__text__004ee6b0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f2880();
        FUN__text__004f2640();
        FUN__text__004f2cb0();
        FUN__text__004f3ae0();
        FUN__text__004f3810();
        FUN__text__004f4200();
        FUN__text__004e7ad0();
        FUN__text__004e7830();
        FUN__text__004e8440();
        FUN__text__004edec0();
        FUN__text__004ed6f0();
        iVar2 = local_10;
      }
      break;
    case 8:
      local_5c = iVar2;
      if (iVar2 < 0x1d52) {
        if (iVar2 == 0x1d51) {
          *(undefined1 *)(local_8 + 0x37) = 4;
          *(undefined1 *)(local_8 + 0x12a) = 1;
          *(undefined2 *)(local_8 + 0x12e) = 0;
          *(undefined1 *)(local_8 + 300) = 0;
        }
        else {
          local_5c = local_10 + -0x1c38;
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
            *(undefined2 *)(local_8 + 0x82) = DAT_00752ea8;
            *(undefined2 *)(local_8 + 0x9c) = DAT_00752eaa;
            break;
          case 0x1c5f:
            *(undefined1 *)(local_8 + 0x3a) = 1;
            *(undefined1 *)(local_8 + 0x52) = 0;
            *(undefined1 *)(local_8 + 0x6a) = 0;
            *(undefined2 *)(local_8 + 0x84) = DAT_00752e78;
            *(undefined2 *)(local_8 + 0x9e) = DAT_00752e7a;
            *(undefined1 *)(local_8 + 0x3b) = 1;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0;
            break;
          case 0x1cc5:
            *(undefined1 *)(local_8 + 0xea) = 1;
            *(undefined2 *)(local_8 + 0xf2) = 0;
            *(undefined2 *)(local_8 + 0x10a) = PTR_DAT_007525a8._0_2_;
            break;
          case 0x1d08:
            *(undefined1 *)(local_8 + 0x3b) = 3;
            *(undefined1 *)(local_8 + 0x53) = 0;
            *(undefined1 *)(local_8 + 0x6b) = 0xff;
          }
        }
      }
      else if (iVar2 < 0x1e6f) {
        if (iVar2 == 0x1e6e) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
        }
        else if (iVar2 == 0x1da2) {
          *(undefined1 *)(local_8 + 0x3c) = 1;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0;
        }
        else if (iVar2 == 0x1e57) {
          *(undefined1 *)(local_8 + 0x3c) = 3;
          *(undefined1 *)(local_8 + 0x54) = 0;
          *(undefined1 *)(local_8 + 0x6c) = 0xff;
        }
      }
      else if (iVar2 == 0x1f73) {
        *(undefined1 *)(local_8 + 0x3d) = 3;
        *(undefined1 *)(local_8 + 0x55) = 0;
        *(undefined1 *)(local_8 + 0x6d) = 0xff;
      }
      else if (iVar2 == 0x1fa9) {
        *(undefined1 *)(local_8 + 0x12a) = 3;
        *(undefined2 *)(local_8 + 0x12e) = 0;
        *(undefined1 *)(local_8 + 300) = 0xff;
      }
      local_10 = iVar2;
      FUN__text__004f4d00();
      FUN__text__004e8f10();
      FUN__text__004ee6b0();
      FUN__text__004f2dc0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f2880();
        FUN__text__004f2640();
        FUN__text__004f3810();
        FUN__text__004f4200();
        FUN__text__004e7ad0();
        FUN__text__004e7830();
        FUN__text__004e8440();
        FUN__text__004edec0();
        FUN__text__004ed6f0();
        iVar2 = local_10;
      }
      break;
    case 9:
      local_60 = local_10 + -0x1fe2;
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
        *(undefined2 *)(local_8 + 0x82) = PTR_DAT_00752d68._0_2_;
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
        *(undefined2 *)(local_8 + 0x84) = PTR_DAT_00752d78._0_2_;
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
        *(undefined2 *)(local_8 + 0x86) = PTR_DAT_00752d88._0_2_;
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
        *(undefined2 *)(local_8 + 0x88) = PTR_DAT_00752d98._0_2_;
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
        *(undefined2 *)(local_8 + 0x8a) = PTR_DAT_00752da8._0_2_;
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
        *(undefined2 *)(local_8 + 0x8c) = PTR_DAT_00752db8._0_2_;
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
        *(undefined2 *)(local_8 + 0x8e) = PTR_DAT_00752dc8._0_2_;
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
        *(undefined2 *)(local_8 + 0x90) = PTR_DAT_00752dd8._0_2_;
      }
      local_10 = iVar2;
      FUN__text__004f2dc0();
      FUN__text__004e8f10();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f2880();
        FUN__text__004e7ad0();
        FUN__text__004e8440();
        iVar2 = local_10;
      }
      break;
    case 10:
      if (iVar2 < 0x21ff) {
        if (iVar2 == 0x21fe) {
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
        }
        else if (iVar2 == 0x20e6) {
          *(undefined1 *)(local_8 + 0x35) = 5;
          *(undefined1 *)(local_8 + 0xea) = 1;
          *(undefined2 *)(local_8 + 0xf2) = 0;
          *(undefined1 *)(local_8 + 0x102) = 0;
          *(undefined2 *)(local_8 + 0x11a) = DAT_007525ca;
          *(undefined1 *)(local_8 + 0xeb) = 1;
          *(undefined2 *)(local_8 + 0xf4) = 0;
          *(undefined1 *)(local_8 + 0x103) = 0;
          *(undefined2 *)(local_8 + 0x11c) = DAT_007525da;
          *(undefined1 *)(local_8 + 0xec) = 1;
          *(undefined2 *)(local_8 + 0xf6) = 0;
          *(undefined1 *)(local_8 + 0x104) = 0;
          *(undefined2 *)(local_8 + 0x11e) = DAT_007525ea;
        }
        else if (iVar2 == 0x2190) {
          *(undefined1 *)(local_8 + 0x34) = 6;
          *(undefined1 *)(local_8 + 0x39) = 1;
          *(undefined1 *)(local_8 + 0x51) = 0;
          *(undefined1 *)(local_8 + 0x69) = 0;
          *(undefined2 *)(local_8 + 0x9c) = DAT_00752bba;
        }
        else if (iVar2 == 0x21d0) {
          *(undefined1 *)(local_8 + 0x3a) = 1;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0;
        }
      }
      else if (iVar2 == 0x2318) {
        *(undefined1 *)(local_8 + 0x3a) = 3;
        *(undefined1 *)(local_8 + 0x52) = 0;
        *(undefined1 *)(local_8 + 0x6a) = 0xff;
      }
      else if (iVar2 == 0x232a) {
        *(undefined1 *)(local_8 + 0xed) = 2;
        *(undefined2 *)(local_8 + 0xf8) = 0;
        *(undefined1 *)(local_8 + 0x105) = 0xff;
        *(undefined2 *)(local_8 + 0x120) = DAT_007525fa;
      }
      else if (iVar2 == 0x2334) {
        *(undefined1 *)(local_8 + 0x3b) = 3;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0xff;
      }
      local_64 = iVar2;
      local_10 = iVar2;
      FUN__text__004f4d00();
      FUN__text__004e8f10();
      FUN__text__004ee6b0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f3810();
        FUN__text__004f3ae0();
        FUN__text__004f4200();
        FUN__text__004e7830();
        FUN__text__004e7ad0();
        FUN__text__004e8440();
        FUN__text__004ed6f0();
        FUN__text__004edec0();
        iVar2 = local_10;
      }
      break;
    case 0xb:
      if (iVar2 < 0x2503) {
        if (iVar2 == 0x2502) {
          *(undefined1 *)(local_8 + 0x3d) = 1;
          *(undefined1 *)(local_8 + 0x55) = 0;
          *(undefined1 *)(local_8 + 0x6d) = 0;
          *(undefined2 *)(local_8 + 0x8a) = DAT_00752e68;
          *(undefined2 *)(local_8 + 0xa4) = DAT_00752e6a;
          local_68 = 0x2502;
        }
        else {
          local_68 = local_10 + -0x241f;
          switch(local_10) {
          case 0x241f:
            *(undefined1 *)(local_8 + 0x34) = 7;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
            *(undefined2 *)(local_8 + 0x82) = DAT_00752e88;
            *(undefined2 *)(local_8 + 0x9c) = DAT_00752e8a;
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
            *(undefined2 *)(local_8 + 0x84) = DAT_00752e58;
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
        local_68 = local_10 + -0x2521;
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
          *(undefined2 *)(local_8 + 0x8c) = DAT_00752de8;
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
          *(undefined2 *)(local_8 + 0x11e) = DAT_0075260a;
        }
      }
      local_10 = iVar2;
      FUN__text__004f4d00();
      FUN__text__004e8f10();
      FUN__text__004ee6b0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f3810();
        FUN__text__004f3ae0();
        FUN__text__004f4200();
        FUN__text__004e7830();
        FUN__text__004e7ad0();
        FUN__text__004e8440();
        FUN__text__004ed6f0();
        FUN__text__004edec0();
        iVar2 = local_10;
      }
      break;
    case 0xc:
      local_6c = local_10 + -0x2675;
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
        *(undefined2 *)(local_8 + 0x84) = DAT_00752eb8;
        *(undefined2 *)(local_8 + 0x9e) = DAT_00752eba;
        break;
      case 0x268d:
        *(undefined1 *)(local_8 + 0x3b) = 1;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0;
        *(undefined2 *)(local_8 + 0x86) = DAT_00752ec8;
        *(undefined2 *)(local_8 + 0xa0) = DAT_00752eca;
        break;
      case 0x2765:
        *(undefined1 *)(local_8 + 0x39) = 3;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0xff;
      }
      local_10 = iVar2;
      FUN__text__004f4d00();
      FUN__text__004e8f10();
      FUN__text__004ee6b0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f3810();
        FUN__text__004f3ae0();
        FUN__text__004f4200();
        FUN__text__004e7830();
        FUN__text__004e7ad0();
        FUN__text__004e8440();
        FUN__text__004ed6f0();
        FUN__text__004edec0();
        iVar2 = local_10;
      }
      break;
    case 0xd:
      if (iVar2 < 0x2a01) {
        if (iVar2 == 0x2a00) {
          *(undefined1 *)(local_8 + 0x3b) = 1;
          *(undefined1 *)(local_8 + 0x53) = 0;
          *(undefined1 *)(local_8 + 0x6b) = 0;
        }
        else if (iVar2 < 0x28f1) {
          if (iVar2 == 0x28f0) {
            *(undefined1 *)(local_8 + 0x12a) = 3;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0xff;
            *(undefined1 *)(local_8 + 0x3a) = 2;
            *(undefined1 *)(local_8 + 0x6a) = 0xff;
            *(undefined2 *)(local_8 + 0x84) = 0x8f;
            *(undefined2 *)(local_8 + 0x9e) = 0x6b;
          }
          else if (iVar2 == 0x27c4) {
            *(undefined1 *)(local_8 + 0x34) = 9;
            *(undefined1 *)(local_8 + 0x39) = 1;
            *(undefined1 *)(local_8 + 0x51) = 0;
            *(undefined1 *)(local_8 + 0x69) = 0;
          }
          else if (iVar2 == 0x28ac) {
            *(undefined1 *)(local_8 + 0x37) = 6;
            *(undefined1 *)(local_8 + 0x12a) = 1;
            *(undefined2 *)(local_8 + 0x12e) = 0;
            *(undefined1 *)(local_8 + 300) = 0;
          }
        }
        else if (iVar2 == 0x29dc) {
          *(undefined1 *)(local_8 + 0x3a) = 3;
          *(undefined1 *)(local_8 + 0x52) = 0;
          *(undefined1 *)(local_8 + 0x6a) = 0xff;
        }
      }
      else if (iVar2 == 0x2a04) {
        *(undefined1 *)(local_8 + 0x3c) = 1;
        *(undefined1 *)(local_8 + 0x54) = 0;
        *(undefined1 *)(local_8 + 0x6c) = 0;
      }
      else if (iVar2 == 0x2a80) {
        *(undefined1 *)(local_8 + 0x3b) = 3;
        *(undefined1 *)(local_8 + 0x53) = 0;
        *(undefined1 *)(local_8 + 0x6b) = 0xff;
        local_28 = '\x03';
        local_2c = CONCAT31(local_2c._1_3_,0xff);
        local_30 = (uint)local_30._1_3_ << 8;
      }
      else if (iVar2 == 0x2a86) {
        *(undefined1 *)(local_8 + 0x3c) = 3;
        *(undefined1 *)(local_8 + 0x54) = 0;
        *(undefined1 *)(local_8 + 0x6c) = 0xff;
      }
      local_70 = iVar2;
      local_10 = iVar2;
      FUN__text__004ee6b0();
      FUN__text__004e8f10();
      FUN__text__004f2dc0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004ed6f0();
        FUN__text__004edec0();
        FUN__text__004e7830();
        FUN__text__004f2880();
        FUN__text__004f2640();
        iVar2 = local_10;
      }
      break;
    case 0xe:
      if (iVar2 < 0x3413) {
        if (iVar2 == 0x3412) {
          *(undefined1 *)(local_8 + 0x41) = 1;
          *(undefined1 *)(local_8 + 0x59) = 0;
          *(undefined1 *)(local_8 + 0x71) = 0;
        }
        else if (iVar2 < 0x2ea3) {
          if (iVar2 == 0x2ea2) {
            *(undefined1 *)(local_8 + 0x3d) = 1;
            *(undefined1 *)(local_8 + 0x55) = 0;
            *(undefined1 *)(local_8 + 0x6d) = 0;
          }
          else if (iVar2 < 0x2c63) {
            if (iVar2 == 0x2c62) {
              *(undefined1 *)(local_8 + 0x3b) = 1;
              *(undefined1 *)(local_8 + 0x53) = 0;
              *(undefined1 *)(local_8 + 0x6b) = 0;
            }
            else if (iVar2 == 0x2aea) {
              *(undefined1 *)(local_8 + 0x34) = 10;
              *(undefined1 *)(local_8 + 0x39) = 1;
              *(undefined1 *)(local_8 + 0x51) = 0;
              *(undefined1 *)(local_8 + 0x69) = 0;
            }
            else if (iVar2 == 0x2b42) {
              *(undefined1 *)(local_8 + 0x3a) = 1;
              *(undefined1 *)(local_8 + 0x52) = 0;
              *(undefined1 *)(local_8 + 0x6a) = 0;
            }
          }
          else if (iVar2 == 0x2d82) {
            *(undefined1 *)(local_8 + 0x3c) = 1;
            *(undefined1 *)(local_8 + 0x54) = 0;
            *(undefined1 *)(local_8 + 0x6c) = 0;
          }
        }
        else if (iVar2 == 0x2fc2) {
          *(undefined1 *)(local_8 + 0x3e) = 1;
          *(undefined1 *)(local_8 + 0x56) = 0;
          *(undefined1 *)(local_8 + 0x6e) = 0;
        }
        else if (iVar2 == 0x30a6) {
          *(undefined1 *)(local_8 + 0x3f) = 1;
          *(undefined1 *)(local_8 + 0x57) = 0;
          *(undefined1 *)(local_8 + 0x6f) = 0;
        }
        else if (iVar2 == 0x323e) {
          *(undefined1 *)(local_8 + 0x40) = 1;
          *(undefined1 *)(local_8 + 0x58) = 0;
          *(undefined1 *)(local_8 + 0x70) = 0;
        }
      }
      else if (iVar2 < 0x3927) {
        if (iVar2 == 0x3926) {
          *(undefined1 *)(local_8 + 0x46) = 1;
          *(undefined1 *)(local_8 + 0x5e) = 0;
          *(undefined1 *)(local_8 + 0x76) = 0;
        }
        else if (iVar2 < 0x3773) {
          if (iVar2 == 0x3772) {
            *(undefined1 *)(local_8 + 0x44) = 1;
            *(undefined1 *)(local_8 + 0x5c) = 0;
            *(undefined1 *)(local_8 + 0x74) = 0;
          }
          else if (iVar2 == 0x3532) {
            *(undefined1 *)(local_8 + 0x42) = 1;
            *(undefined1 *)(local_8 + 0x5a) = 0;
            *(undefined1 *)(local_8 + 0x72) = 0;
          }
          else if (iVar2 == 0x3652) {
            *(undefined1 *)(local_8 + 0x43) = 1;
            *(undefined1 *)(local_8 + 0x5b) = 0;
            *(undefined1 *)(local_8 + 0x73) = 0;
          }
        }
        else if (iVar2 == 0x3892) {
          *(undefined1 *)(local_8 + 0x45) = 1;
          *(undefined1 *)(local_8 + 0x5d) = 0;
          *(undefined1 *)(local_8 + 0x75) = 0;
        }
      }
      else if (iVar2 == 0x3a82) {
        *(undefined1 *)(local_8 + 0x47) = 1;
        *(undefined1 *)(local_8 + 0x5f) = 0;
        *(undefined1 *)(local_8 + 0x77) = 0;
      }
      else if (iVar2 == 0x3b66) {
        *(undefined1 *)(local_8 + 0x48) = 1;
        *(undefined1 *)(local_8 + 0x60) = 0;
        *(undefined1 *)(local_8 + 0x78) = 0;
      }
      else if (iVar2 == 0x3cc2) {
        *(undefined1 *)(local_8 + 0x48) = 3;
        *(undefined1 *)(local_8 + 0x60) = 0;
        *(undefined1 *)(local_8 + 0x78) = 0xff;
      }
      local_74 = iVar2;
      local_10 = iVar2;
      FUN__text__004e8f10();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004e7830();
        FUN__text__004e7ad0();
        iVar2 = local_10;
      }
      break;
    case 0xf:
      if (iVar2 == 0x3d30) {
        *(undefined1 *)(local_8 + 0x34) = 0xb;
        *(undefined1 *)(local_8 + 0x39) = 1;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0;
      }
      else if (iVar2 == 0x3eae) {
        *(undefined1 *)(local_8 + 0x39) = 3;
        *(undefined1 *)(local_8 + 0x51) = 0;
        *(undefined1 *)(local_8 + 0x69) = 0xff;
      }
      local_78 = iVar2;
      local_10 = iVar2;
      FUN__text__004ee6b0();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004ed6f0();
        FUN__text__004edec0();
        iVar2 = local_10;
      }
      break;
    case 0x10:
      if (iVar2 == 0x3f56) {
        *(undefined1 *)(local_8 + 0x35) = 8;
        *(undefined1 *)(local_8 + 0xea) = 1;
        *(undefined2 *)(local_8 + 0xf2) = 0;
        *(undefined1 *)(local_8 + 0x102) = 0;
      }
      else if (iVar2 == 0x4526) {
        *(undefined1 *)(local_8 + 0xea) = 3;
        *(undefined2 *)(local_8 + 0xf2) = 0;
        *(undefined1 *)(local_8 + 0x102) = 0xff;
      }
      local_7c = iVar2;
      local_10 = iVar2;
      FUN__text__004f4d00();
      iVar2 = local_10;
      if (local_14 == 0) {
        FUN__text__004f3810();
        FUN__text__004f3ae0();
        iVar2 = local_10;
      }
      break;
    case 0x11:
      local_80 = iVar2;
      if (iVar2 == 0x459e) {
        *(undefined1 *)(local_8 + 0x32) = 100;
      }
      break;
    case 100:
      goto switchD__text__004e40c9_caseD_64;
    }
    local_10 = iVar2;
    FUN__text__00422360(0);
    if ((*(uint *)(DAT_007a49fc + 0x1950) & 0x8000) != 0) {
      FUN__text__00422360(0);
      FUN__text__00422360(0);
      FUN__text__0041e500();
      FUN__text__0041f4e0(10);
      for (local_c = 0; local_c != 10; local_c = local_c + 1) {
        FUN__text__00464d30();
      }
      *(undefined4 *)(DAT_007a4a00 + 0x8e0) = 1;
      local_8 = 0x4e6cfa;
      FUN__text__0056ce80();
      return;
    }
  } while( true );
switchD__text__004e40c9_caseD_64:
  local_10 = iVar2;
  FUN__text__0041e500();
  FUN__text__00422360(0);
  goto LAB__text__004e3b78;
}

