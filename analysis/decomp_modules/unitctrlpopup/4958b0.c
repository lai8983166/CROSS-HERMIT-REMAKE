
void FUN__text__004958b0(byte *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  uint local_18;
  undefined *local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((*param_1 & 0x80) == 0) &&
     (iVar2 = FUN__text__00424f80("(pw->mode & 0x80)!=0",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                  DAT_00619f5c + 4,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*param_1 & 0x80) != 0) {
    local_c = *(int *)(param_1 + 0xc) + (char)param_1[10] * 8;
    local_14 = &DAT_00619748 + *(char *)(local_c + 4) * 0x12;
    *(short *)(param_1 + 6) = *(short *)(param_1 + 6) + -1;
    if (*(short *)(param_1 + 6) < 1) {
      if ((*(byte *)(local_c + 2) & 0x80) != 0) goto switchD__text__004959cb_default;
      param_1[10] = param_1[10] + 1;
      local_10 = *(int *)(param_1 + 0xc) + (char)param_1[10] * 8;
      *(undefined2 *)(param_1 + 6) = *(undefined2 *)(local_10 + 6);
    }
    local_18 = (uint)param_1[1];
    switch(local_18) {
    case 0:
    case 1:
    case 4:
    case 5:
    case 9:
    case 10:
    case 0xd:
    case 0xe:
      if (('\x03' < (char)param_1[10]) && (param_1[0xb] + 8 < 0xff)) {
        param_1[3] = param_1[3] - 2;
        param_1[0xb] = param_1[0xb] + 4;
      }
      break;
    case 2:
    case 3:
    case 0xb:
    case 0xc:
      if (('\x03' < (char)param_1[10]) && (param_1[0xb] + 3 < 0xff)) {
        param_1[3] = param_1[3] - 1;
        param_1[0xb] = param_1[0xb] + 3;
      }
      break;
    case 6:
    case 7:
    case 8:
    case 0xf:
    case 0x10:
    case 0x11:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlPopup.cpp",
                                  DAT_00619f5c + 0x35,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
switchD__text__004959cb_default:
  local_8 = 0x495a8a;
  FUN__text__0056ce80();
  return;
}

