
void FUN__text__0048e1f0(byte *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *param_1 - 1;
  switch(*param_1) {
  case 1:
  case 3:
  case 4:
  case 5:
  case 6:
  case 8:
  case 0xb:
  case 0xc:
    break;
  case 2:
  case 7:
  case 0xf:
  case 0x10:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                DAT_00618fa0 + 0x12,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  default:
  }
  local_8 = 0x48e27b;
  FUN__text__0056ce80();
  return;
}

