
void FUN__text__00482d60(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                        undefined4 param_5)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  short *local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  param_1 = param_1 * 6;
  local_c = (short *)(&DAT_00613b78 + param_1);
  local_14 = param_2;
  switch(param_2) {
  case 0:
    FUN__text__004950c0(param_3);
    goto LAB__text__00482e79;
  case 1:
    local_10 = (int)*(short *)(&DAT_00613b7a + param_1);
    break;
  case 2:
    local_10 = (int)*(short *)(&DAT_00613b7a + param_1);
    break;
  case 3:
    local_10 = (int)*(short *)(&DAT_00613b7c + param_1);
    break;
  case 4:
    local_10 = (int)*local_c;
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_0059d9a8,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f08 + 0xf,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_18 = local_10 + -0x7d1;
  switch(local_10) {
  case 0x7d1:
  case 0x7d7:
  case 0x7dc:
  case 0x7e2:
  case 0x7e7:
  case 0x7ed:
  case 0x804:
  case 0x809:
    iVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f08 + 0x1c);
    local_10 = local_10 + iVar2 % 5;
  }
  FUN__text__0046beb0(param_4,local_10,0,0,0,param_5);
LAB__text__00482e79:
  local_8 = 0x482e86;
  FUN__text__0056ce80();
  return;
}

