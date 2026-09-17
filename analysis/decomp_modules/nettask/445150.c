
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__00445150(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_ec [16];
  int local_ac;
  int local_a8;
  int local_a4;
  undefined1 local_a0 [4];
  undefined1 local_9c [128];
  int local_1c;
  short local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_ec;
  for (iVar2 = 0x3a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  _DAT_007a3f9c = 1;
  local_1c = param_1 + 0x1a54;
  local_8 = param_1;
  FUN__text__00428220(0,1);
  FUN__text__00446290(local_8 + 0x8a58);
  _memset((void *)(local_8 + 0x1bb0),0,0x10);
  *(undefined4 *)(local_8 + 0x1bc8) = 0;
  local_c = FUN__text__004180b0();
  if (local_c == 0) {
    if (*(int *)(local_8 + 0x1a54) == 0) {
      iVar2 = FUN__text__004183e0(&DAT_005953ac);
      if (iVar2 != 0) {
        *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
        *(undefined4 *)(local_8 + 0x1bc4) = 1;
        *(undefined4 *)(local_8 + 0x1bc8) = 1;
        goto LAB__text__0044537c;
      }
    }
    else {
      FUN__text__0056d810(local_9c,"%d.%d.%d.%d",*(uint *)(DAT_007a4a00 + 0x110c) >> 0x18,
                          *(uint *)(DAT_007a4a00 + 0x110c) >> 0x10 & 0xff,
                          *(uint *)(DAT_007a4a00 + 0x110c) >> 8 & 0xff,
                          *(uint *)(DAT_007a4a00 + 0x110c) & 0xff);
      iVar2 = FUN__text__004183e0(local_9c);
      if (iVar2 != 0) {
        *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
        *(undefined4 *)(local_8 + 0x1bc4) = 1;
        *(undefined4 *)(local_8 + 0x1bc8) = 1;
        goto LAB__text__0044537c;
      }
    }
    local_c = FUN__text__004188b0();
    local_a4 = FUN__text__00418900();
    local_c = local_a4;
    if ((local_a4 < 0) || (1 < local_a4)) {
      *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
      *(undefined4 *)(local_8 + 0x1bc4) = 2;
    }
  }
  else {
    *(undefined4 *)(local_8 + 0x1bb0) = 0xff;
    *(undefined4 *)(local_8 + 0x1bc4) = 0;
    *(undefined4 *)(local_8 + 0x1bc8) = 1;
  }
LAB__text__0044537c:
  local_14 = 1;
  do {
    if (local_14 == 0) {
      local_8 = 0x4457ab;
      FUN__text__0056ce80();
      return;
    }
    local_a8 = *(int *)(local_8 + 0x1bb0);
    if (local_a8 < 3) {
      if (local_a8 == 2) {
        iVar2 = FUN__text__00445920();
        if (iVar2 != 0) {
          local_14 = 0;
        }
      }
      else if (local_a8 == 0) {
        local_10 = FUN__text__0044c710(&DAT_00605aa8,0xf);
        if ((local_10 == -1) || ((*(uint *)(DAT_007a49fc + 0x199c) & 1) == 0)) {
          iVar2 = FUN__text__004128f0(0xc9,2);
          if (iVar2 == 0) {
            iVar2 = FUN__text__004128f0(200,2);
            if (iVar2 == 0) {
              iVar2 = FUN__text__004128f0(0xd0,2);
              if (iVar2 == 0) {
                iVar2 = FUN__text__004128f0(0xd1,2);
                if (iVar2 != 0) {
                  FUN__text__00428760();
                  FUN__text__004db2b0(5);
                }
              }
              else {
                FUN__text__004285f0();
                FUN__text__004db2b0(5);
              }
            }
            else {
              FUN__text__00428520();
              FUN__text__004db2b0(5);
            }
          }
          else {
            FUN__text__00428720();
            FUN__text__004db2b0(5);
          }
        }
        else {
          local_ac = local_10;
          switch(local_10) {
          case 0:
            *(undefined4 *)(local_8 + 0x1bb0) = 2;
            *(undefined4 *)(local_8 + 0x1bb4) = 0;
            FUN__text__004db2b0(5);
            break;
          case 1:
            *(undefined4 *)(local_8 + 0x1bb0) = 3;
            *(undefined4 *)(local_8 + 0x1bb4) = 0;
            FUN__text__004db2b0(5);
            break;
          case 2:
            *(undefined4 *)(local_8 + 0x1bb0) = 1;
            *(undefined4 *)(local_8 + 0x1bb4) = 0;
            FUN__text__004db2b0(5);
            break;
          case 3:
            FUN__text__00418a00();
            FUN__text__004db2b0(2);
LAB__text__0044573d:
            *(undefined4 *)(local_8 + 0x1a50) = 2;
            local_14 = 0;
            goto LAB__text__00445760;
          case 4:
            FUN__text__00428720();
            FUN__text__004db2b0(5);
            break;
          case 5:
            FUN__text__00428520();
            FUN__text__004db2b0(5);
            break;
          case 6:
            FUN__text__004285f0();
            FUN__text__004db2b0(5);
            break;
          case 7:
            FUN__text__00428760();
            FUN__text__004db2b0(5);
            break;
          case 8:
          case 9:
          case 10:
          case 0xb:
          case 0xc:
          case 0xd:
          case 0xe:
          case 0xf:
            local_18 = (short)local_10 + -8;
            FUN__text__004282b0(local_18);
            break;
          default:
            iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                        DAT_0060671c + 0x91,0);
            if (iVar2 != 0) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
        }
        if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
          local_10 = -1;
        }
        FUN__text__00446340(local_10,0xff);
        FUN__text__0044ca80();
        FUN__text__0044c9a0(0);
      }
      else if ((local_a8 == 1) && (iVar2 = FUN__text__00445800(), iVar2 != 0)) {
        local_14 = 0;
      }
    }
    else if (local_a8 == 3) {
      iVar2 = FUN__text__00445c10();
      if (iVar2 != 0) {
        local_14 = 0;
      }
    }
    else if (local_a8 == 0xff) {
      iVar2 = FUN__text__00441630(*(undefined4 *)(local_8 + 0x1bc4),local_a0,0x200,0x180,0x3c);
      if (iVar2 != 0) {
        if (*(int *)(local_8 + 0x1bc8) != 0) goto LAB__text__0044573d;
        *(undefined4 *)(local_8 + 0x1bb0) = 0;
      }
LAB__text__00445760:
      FUN__text__00446340(0xffffffff,0x40);
      FUN__text__0044ca80();
      FUN__text__0044c9a0(0);
    }
    FUN__text__00422360(0);
  } while( true );
}

