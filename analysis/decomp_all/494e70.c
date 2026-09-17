
void FUN__text__00494e70(int param_1,undefined2 param_2,undefined4 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__00494db0();
  if (local_c != 0) {
    *(undefined2 *)(local_c + 4) = *(undefined2 *)(param_1 + 2);
    local_10 = param_3;
    switch(param_3) {
    case 0:
      *(undefined1 *)(local_c + 1) = 0;
      break;
    case 1:
      *(undefined1 *)(local_c + 1) = 1;
      break;
    case 2:
      *(undefined1 *)(local_c + 1) = 2;
      break;
    case 3:
      *(undefined1 *)(local_c + 1) = 3;
      break;
    case 4:
      *(undefined1 *)(local_c + 1) = 4;
      break;
    case 5:
      *(undefined1 *)(local_c + 1) = 5;
      break;
    case 6:
      *(undefined1 *)(local_c + 1) = 6;
      break;
    case 7:
      *(undefined1 *)(local_c + 1) = 7;
      break;
    case 8:
      *(undefined1 *)(local_c + 1) = 8;
      break;
    case 9:
      *(undefined1 *)(local_c + 1) = 9;
      break;
    case 10:
      *(undefined1 *)(local_c + 1) = 10;
      break;
    case 0xb:
      *(undefined1 *)(local_c + 1) = 0xb;
      break;
    case 0xc:
      *(undefined1 *)(local_c + 1) = 0xc;
      break;
    case 0xd:
      *(undefined1 *)(local_c + 1) = 0xd;
      break;
    case 0xe:
      *(undefined1 *)(local_c + 1) = 0xe;
      break;
    case 0xf:
      *(undefined1 *)(local_c + 1) = 0xf;
      break;
    case 0x10:
      *(undefined1 *)(local_c + 1) = 0x10;
      break;
    case 0x11:
      *(undefined1 *)(local_c + 1) = 0x11;
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                  DAT_00619f50 + 0x18,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    *(undefined2 *)(local_c + 8) = param_2;
    if (*(short *)(local_c + 8) < 0) {
      *(short *)(local_c + 8) = -*(short *)(local_c + 8);
    }
    FUN__text__00495630(local_c);
  }
  local_8 = 0x494ff3;
  FUN__text__0056ce80();
  return;
}

