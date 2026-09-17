
void FUN__text__00495320(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (uint)*(byte *)(param_1 + 1);
  switch(local_c) {
  case 0:
  case 1:
  case 2:
  case 3:
  case 4:
  case 5:
    FUN__text__004954f0(param_1);
    break;
  case 6:
  case 7:
  case 8:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                DAT_00619f54 + 0xc,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 9:
  case 10:
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
    FUN__text__004954f0(param_1);
    break;
  case 0xf:
  case 0x10:
  case 0x11:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                DAT_00619f54 + 0x17,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 0x12:
    FUN__text__00495540(param_1);
    break;
  case 0x13:
    FUN__text__00495590(param_1);
    break;
  case 0x14:
  case 0x15:
  case 0x16:
  case 0x17:
  case 0x28:
  case 0x29:
  case 0x2a:
  case 0x2b:
  case 0x2c:
  case 0x2d:
  case 0x2e:
  case 0x2f:
  case 0x30:
  case 0x31:
  case 0x32:
  case 0x33:
  case 0x34:
  case 0x35:
  case 0x36:
  case 0x37:
    FUN__text__004955e0(param_1);
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                DAT_00619f54 + 0x3e,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 0x38:
  case 0x39:
  case 0x3a:
  case 0x3b:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                DAT_00619f54 + 0x3b,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x49547d;
  FUN__text__0056ce80();
  return;
}

