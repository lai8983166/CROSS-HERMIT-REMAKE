
void __thiscall FUN__text__004919f0(int param_1,int param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  uint local_28;
  uint local_24;
  int local_20;
  uint local_1c;
  undefined *local_18;
  undefined *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((0xf9 < *(byte *)(param_4 + 2)) &&
     (iVar2 = FUN__text__00424f80("(0<=data->from) && (data->from<(250))",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                  DAT_00619240 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((0xf9 < *(byte *)(param_4 + 3)) &&
     (iVar2 = FUN__text__00424f80("(0<=data->to ) && (data->to <(250))",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                  DAT_00619240 + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = local_8 + 0x80aec + (uint)*(byte *)(param_4 + 2) * 0x520;
  local_10 = local_8 + 0x80aec + (uint)*(byte *)(param_4 + 3) * 0x520;
  iVar2 = FUN__text__004690a0(local_c);
  if ((iVar2 == 0) && (iVar2 = FUN__text__004690a0(local_10), iVar2 == 0)) {
    *(ushort *)(*(int *)(param_2 + 600) + 0xa6) = (ushort)*(byte *)(param_4 + 2);
    local_1c = (uint)*(ushort *)(*(int *)(local_10 + 600) + 0xc);
    if (local_1c == 0x1c6) {
      if (*(short *)(param_4 + 4) < 100) {
        if (*(char *)(param_4 + 6) != '\x04') {
          FUN__text__00493090(local_10,0,0);
        }
        goto switchD__text__00491c06_default;
      }
    }
    else if ((local_1c == 0x1c7) && (99 < *(short *)(param_4 + 4))) {
      if (*(char *)(param_4 + 6) != '\x04') {
        FUN__text__00493090(local_10,0,0);
      }
      goto switchD__text__00491c06_default;
    }
    local_20 = (int)*(short *)(param_4 + 4);
    FUN__text__00491ef0(local_c,local_10,param_4);
    iVar2 = FUN__text__00469b90(param_2);
    if ((iVar2 == 0) && (iVar2 = FUN__text__00469c60(param_2), iVar2 == 0)) {
      local_24 = (uint)*(byte *)(param_4 + 6);
      switch(local_24) {
      case 0:
        FUN__text__0049ad90(param_2,0x94);
      case 1:
        if (*(short *)(param_4 + 10) < 1) {
          FUN__text__0049ad90(param_2,0x95);
        }
        *(undefined2 *)(local_10 + 0x4fa) = *(undefined2 *)(local_c + 2);
        break;
      case 2:
        if (*(short *)(param_4 + 10) < 1) {
          FUN__text__0049ad90(param_2,0x6c);
        }
        iVar2 = FUN__text__004692e0(param_2);
        if (iVar2 == 0) {
          iVar2 = FUN__text__00469730(param_2);
          if (iVar2 == 0) {
            FUN__text__004753f0(param_2);
          }
          FUN__text__00437d90(param_2,0);
          FUN__text__00475270(param_2,8);
          *(undefined2 *)(param_2 + 0x4f8) = *(undefined2 *)(local_c + 2);
        }
        FUN__text__00492de0(local_c,local_10);
        break;
      case 3:
        if (*(short *)(param_4 + 10) < 1) {
          FUN__text__0049ad90(param_2,0x6d);
        }
        if (((((DAT_007f4488 != 7) && (DAT_007f4488 != 0x4c)) ||
             (*(short *)(*(int *)(param_2 + 600) + 2) != 6)) ||
            (*(char *)(*(int *)(param_2 + 600) + 0xa4) != '\x04')) &&
           (iVar2 = FUN__text__004692e0(param_2), iVar2 == 0)) {
          iVar2 = FUN__text__00469730(param_2);
          if (iVar2 == 0) {
            FUN__text__004753f0(param_2);
          }
          FUN__text__00437d90(param_2,0);
          iVar2 = (uint)*(ushort *)(*(int *)(local_10 + 600) + 0xc) * 0x40;
          local_14 = &DAT_006b2d88 + iVar2;
          if ((&DAT_006b2da9)[iVar2] == 'd') {
            *(undefined1 *)(param_2 + 0x4f6) = 0xff;
          }
          else {
            iVar2 = FUN__text__0046c9f0((int)*(short *)(param_4 + 4));
            if (iVar2 == 0) {
              iVar2 = *(short *)(param_4 + 4) * 0x48;
              local_18 = &DAT_006c2dc8 + iVar2;
              local_28 = (uint)(byte)(&DAT_006c2de0)[iVar2];
              switch(local_28) {
              case 0:
              case 5:
                *(undefined1 *)(param_2 + 0x4f6) = 0xff;
                break;
              case 1:
              case 2:
              case 3:
              case 6:
                *(undefined1 *)(param_2 + 0x4f6) = 1;
                break;
              case 4:
                *(undefined1 *)(param_2 + 0x4f4) = *(undefined1 *)(param_4 + 8);
                *(undefined1 *)(param_2 + 0x4f5) = *(undefined1 *)(param_4 + 9);
                *(undefined1 *)(param_2 + 0x4f6) = 0;
              }
            }
            else {
              *(undefined1 *)(param_2 + 0x4f6) = 1;
            }
          }
          FUN__text__00475270(param_2,9);
          *(undefined2 *)(param_2 + 0x4f8) = *(undefined2 *)(local_c + 2);
        }
        FUN__text__00492de0(local_c,local_10);
        break;
      case 4:
        FUN__text__0049ad90(param_2,0x6e);
        FUN__text__00495050(param_2);
        FUN__text__00492de0(local_c,local_10);
      }
    }
  }
switchD__text__00491c06_default:
  local_8 = 0x491eb6;
  FUN__text__0056ce80();
  return;
}

