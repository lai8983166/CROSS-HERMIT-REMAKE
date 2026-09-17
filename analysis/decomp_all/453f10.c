
void __fastcall FUN__text__00453f10(int param_1)

{
  code *pcVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_64 [16];
  undefined4 local_24;
  int local_20;
  undefined4 local_1c;
  undefined4 local_18;
  short local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_64;
  for (iVar3 = 0x18; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_18 = *(undefined4 *)(param_1 + 0x38);
  local_8 = param_1;
  switch(local_18) {
  case 0:
    *(undefined2 *)(param_1 + 0x108cc2) = 1;
    *(undefined4 *)(param_1 + 0x38) = 3;
    DAT_007a417c = -0x400;
    DAT_007a4184 = 0;
  case 3:
    local_10 = 0;
    for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
      local_14 = DAT_007a417c + (short)(local_c << 4);
      if (local_14 < 0) {
        local_14 = 0;
      }
      if (0xff < local_14) {
        local_14 = 0xff;
      }
      local_14 = 0xff - local_14;
      FUN__text__00410310(0,local_10 * 6,0x400,6,5,(int)local_14 << 0x18,1);
      FUN__text__00410310(0,(0x3f - local_10) * 6 + 0x180,0x400,6,5,(int)local_14 << 0x18,1);
      local_10 = local_10 + 1;
    }
    sVar2 = FUN__text__00415040(6);
    DAT_007a417c = DAT_007a417c + sVar2;
    if (0xfe < DAT_007a417c) {
      DAT_007a4184 = 0;
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    }
    break;
  case 1:
    local_10 = 0;
    for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
      local_14 = DAT_007a417c + (short)(local_c << 4);
      if (local_14 < 0) {
        local_14 = 0;
      }
      if (0xff < local_14) {
        local_14 = 0xff;
      }
      local_14 = 0xff - local_14;
      FUN__text__00410310(local_10 << 4,0,0x10,0x300,5,(int)local_14 << 0x18,1);
      local_10 = local_10 + 1;
    }
    sVar2 = FUN__text__00415040(8);
    DAT_007a417c = DAT_007a417c + sVar2;
    if (0xff < DAT_007a417c) {
      DAT_007a417c = -0x400;
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    }
    break;
  case 2:
    local_10 = 0x3f;
    for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
      local_14 = DAT_007a417c + (short)(local_c << 4);
      if (local_14 < 0) {
        local_14 = 0;
      }
      if (0xff < local_14) {
        local_14 = 0xff;
      }
      FUN__text__00410310(local_10 << 4,0,0x10,0x300,5,(int)local_14 << 0x18,1);
      local_10 = local_10 + -1;
    }
    sVar2 = FUN__text__00415040(8);
    DAT_007a417c = DAT_007a417c + sVar2;
    if (0xff < DAT_007a417c) {
      DAT_007a417c = -0x400;
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    }
    break;
  case 4:
    *(undefined1 *)(param_1 + 0x170) = 1;
    *(undefined1 *)(param_1 + 0x171) = 0;
    *(int *)(param_1 + 0x38) = *(int *)(param_1 + 0x38) + 1;
    break;
  case 5:
    if (*(char *)(param_1 + 0x171) != '\0') {
      *(undefined2 *)(param_1 + 0x108cc2) = 0;
      *(undefined4 *)(param_1 + 0x38) = 0xf;
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x170) != '\0') {
      *(undefined1 *)(param_1 + 0x170) = 0;
      *(int *)(param_1 + 0x38) = *(int *)(param_1 + 0x38) + 1;
    }
    break;
  case 7:
    FUN__text__004998b0(0);
    *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    break;
  case 8:
    iVar3 = FUN__text__00499910();
    if (iVar3 != 0) {
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    }
    break;
  case 9:
    FUN__text__004998b0(1);
    *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    break;
  case 10:
    iVar3 = FUN__text__00499910();
    if (iVar3 != 0) {
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    }
    break;
  case 0xb:
    DAT_007a4184 = 0xff;
    *(int *)(param_1 + 0x38) = *(int *)(param_1 + 0x38) + 1;
    break;
  case 0xc:
    sVar2 = FUN__text__00415040(4);
    DAT_007a4184 = DAT_007a4184 - sVar2;
    if (DAT_007a4184 < 1) {
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    }
    *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    break;
  case 0xd:
    *(undefined1 *)(param_1 + 0x170) = 1;
    *(undefined2 *)(param_1 + 0x108cc2) = 1;
    *(undefined1 *)(param_1 + 0x171) = 0;
    *(int *)(param_1 + 0x38) = *(int *)(param_1 + 0x38) + 1;
    break;
  case 0xe:
    if (*(char *)(param_1 + 0x171) != '\0') {
      *(undefined2 *)(param_1 + 0x108cc2) = 0;
      *(int *)(param_1 + 0x38) = *(int *)(param_1 + 0x38) + 1;
    }
    break;
  case 0xf:
    DAT_007a4184 = 0;
    *(int *)(param_1 + 0x38) = *(int *)(param_1 + 0x38) + 1;
    break;
  case 0x10:
    sVar2 = FUN__text__00415040(4);
    DAT_007a4184 = DAT_007a4184 + sVar2;
    if (0xfe < DAT_007a4184) {
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
      local_1c = *(undefined4 *)(local_8 + 0x174);
      switch(local_1c) {
      case 0:
        *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
        break;
      case 1:
        FUN__text__004998b0(2);
        DAT_005ff720 = 0;
        break;
      case 2:
        FUN__text__004998b0(3);
        DAT_005ff720 = 1;
        break;
      case 3:
        FUN__text__004998b0(4);
        DAT_005ff720 = 1;
        break;
      case 4:
        FUN__text__004998b0(5);
        DAT_005ff720 = 2;
        break;
      case 5:
        FUN__text__004998b0(6);
        DAT_005ff720 = 2;
        break;
      default:
        iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                    DAT_0060cd84 + 0xb5,0);
        if (iVar3 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      local_20 = (int)DAT_007f4488;
      if (local_20 == 0x2d) {
        local_24 = *(undefined4 *)(local_8 + 0x174);
        switch(local_24) {
        case 0:
          break;
        case 1:
          break;
        case 2:
          break;
        case 3:
          break;
        case 4:
          FUN__text__004998b0(0xc);
          break;
        case 5:
          FUN__text__004998b0(0xc);
          break;
        default:
          iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                      DAT_0060cd84 + 0xc1,0);
          if (iVar3 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
      }
    }
    break;
  case 0x11:
    iVar3 = FUN__text__00499910();
    if (iVar3 != 0) {
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
    }
    break;
  case 0x12:
    DAT_007a417c = 0x4ff;
    *(int *)(param_1 + 0x38) = *(int *)(param_1 + 0x38) + 1;
    break;
  case 0x13:
    local_10 = 0x3f;
    for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
      local_14 = 0xff - (DAT_007a417c - (short)(local_c << 4));
      if (local_14 < 0) {
        local_14 = 0;
      }
      if (0xff < local_14) {
        local_14 = 0xff;
      }
      FUN__text__00410310(0,local_10 * 6,0x400,6,5,(int)local_14 << 0x18,1);
      FUN__text__00410310(0,(0x3f - local_10) * 6 + 0x180,0x400,6,5,(int)local_14 << 0x18,1);
      local_10 = local_10 + -1;
    }
    sVar2 = FUN__text__00415040(6);
    DAT_007a417c = DAT_007a417c - sVar2;
    if (DAT_007a417c < 0) {
      *(int *)(local_8 + 0x38) = *(int *)(local_8 + 0x38) + 1;
      FUN__text__00473860();
    }
    break;
  case 0x14:
  }
  local_8 = 0x4547be;
  FUN__text__0056ce80();
  return;
}

