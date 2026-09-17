
void FUN__text__0047aed0(int param_1,int param_2,int param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_3 == 0) &&
     (iVar2 = FUN__text__00424f80("dst!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e38 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (param_2 != 0) {
    local_14 = param_4 + -1;
    switch(local_14) {
    case 0:
      break;
    case 1:
      break;
    case 2:
      break;
    case 3:
      break;
    case 4:
      break;
    case 5:
      break;
    case 6:
      break;
    case 7:
      break;
    case 8:
      iVar2 = FUN__text__0056db00(*(int *)(param_2 + 0x2ec) - *(int *)(param_1 + 0x2ec));
      local_c = FUN__text__0056db00(*(int *)(param_2 + 0x2f0) - *(int *)(param_1 + 0x2f0));
      local_c = iVar2 + local_c;
      iVar2 = FUN__text__0056db00(*(int *)(param_3 + 0x2ec) - *(int *)(param_1 + 0x2ec));
      local_10 = FUN__text__0056db00(*(int *)(param_3 + 0x2f0) - *(int *)(param_1 + 0x2f0));
      local_10 = iVar2 + local_10;
      break;
    case 9:
      iVar2 = FUN__text__0056db00(*(int *)(param_2 + 0x2ec) - *(int *)(param_1 + 0x2ec));
      local_c = FUN__text__0056db00(*(int *)(param_2 + 0x2f0) - *(int *)(param_1 + 0x2f0));
      local_c = iVar2 + local_c;
      iVar2 = FUN__text__0056db00(*(int *)(param_3 + 0x2ec) - *(int *)(param_1 + 0x2ec));
      local_10 = FUN__text__0056db00(*(int *)(param_3 + 0x2f0) - *(int *)(param_1 + 0x2f0));
      local_10 = iVar2 + local_10;
    }
  }
  local_8 = 0x47b1db;
  FUN__text__0056ce80();
  return;
}

