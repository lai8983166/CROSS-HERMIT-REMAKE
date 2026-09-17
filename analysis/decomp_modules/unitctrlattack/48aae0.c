
void FUN__text__0048aae0(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__0046abc0(param_1,param_2);
  if ((iVar2 != 0) || (iVar2 = FUN__text__0046ad60(param_1,param_2), iVar2 != 0)) {
    if (*(short *)(param_4 + 2) != 5) goto switchD__text__0048ab9d_default;
    iVar2 = FUN__text__00469a30(param_1);
    if ((iVar2 == 0) ||
       (iVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f70 + 7), iVar2 % 0x32 == 0)) {
      FUN__text__0048b1b0(param_1,param_2,param_3);
      goto switchD__text__0048ab9d_default;
    }
  }
  local_c = (uint)*(byte *)(param_4 + 0x18);
  switch(local_c) {
  case 0:
  case 4:
  case 5:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f70 + 0x16,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 1:
  case 2:
  case 3:
    local_10 = (uint)*(byte *)(param_4 + 5);
    switch(local_10) {
    case 0:
    case 3:
      FUN__text__0048ac90(param_1,param_2,param_3);
      break;
    case 1:
    case 4:
      FUN__text__0048ac90(param_1,param_2,param_3);
      break;
    case 2:
      FUN__text__0048b080(param_1,param_2,param_3);
    }
    break;
  case 6:
    FUN__text__0048adc0(param_1,param_2,param_3);
  }
switchD__text__0048ab9d_default:
  local_8 = 0x48ac5a;
  FUN__text__0056ce80();
  return;
}

