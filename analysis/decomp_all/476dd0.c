
void FUN__text__00476dd0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  undefined4 local_28;
  int local_24;
  char local_20;
  int local_1c;
  int local_18;
  char *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_14 = (char *)(param_1 + 0x293);
  local_20 = *local_14;
  if (local_20 == '\0') {
    *(undefined1 *)(param_1 + 0x294) = 0;
    *(undefined2 *)(param_1 + 0x4e0) = 0;
    *local_14 = *local_14 + '\x01';
  }
  else if (local_20 == '\x01') {
    iVar2 = FUN__text__004698a0(param_1);
    if (iVar2 != 0) {
      iVar2 = FUN__text__0047b790(param_1);
      if ((iVar2 != 0) && (iVar2 = FUN__text__0047b920(param_1,param_1 + 0x4fc), iVar2 != 0))
      goto LAB__text__00477189;
      iVar2 = FUN__text__0047cc90(param_1);
      if (iVar2 != 0) {
        local_18 = local_8 + 0x80aec + *(short *)(param_1 + 0x4fa) * 0x520;
        iVar2 = FUN__text__0047ce70(param_1,local_18);
        if (iVar2 != 0) {
          FUN__text__00437d90(param_1,0);
          goto LAB__text__00477189;
        }
      }
      iVar2 = FUN__text__00480480(param_1);
      if (iVar2 != 0) {
        iVar2 = FUN__text__00468d80(param_1);
        if ((iVar2 != 0) &&
           (iVar2 = FUN__text__00424f80("IsUwHuman(wk)==0",
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                        DAT_00618e04 + 0x27,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        iVar2 = FUN__text__00469ad0(param_1);
        if ((iVar2 != 0) &&
           (iVar2 = FUN__text__00424f80("IsUwBaseUnit(wk)==0",
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                        DAT_00618e04 + 0x28,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        FUN__text__00475270(param_1,0x18);
        FUN__text__00437d90(param_1,0);
        goto LAB__text__00477189;
      }
      local_1c = FUN__text__0047a920(param_1);
      if (local_1c != 0) {
        local_10 = FUN__text__0047a8e0(param_1);
        local_24 = (int)*(char *)(local_10 + 0x12);
        switch(local_24) {
        case 0:
          iVar2 = FUN__text__0047c580(param_1,local_1c);
          if (iVar2 != 0) {
            FUN__text__00475270(param_1,6);
            FUN__text__00437d90(param_1,0);
            goto LAB__text__00477189;
          }
          break;
        case 2:
          *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(local_1c + 2);
          FUN__text__00475270(param_1,0x1d);
          FUN__text__00437d90(param_1,0);
          break;
        case 3:
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e04 + 0x4c,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
          break;
        case 4:
          FUN__text__00475270(param_1,6);
          FUN__text__00437d90(param_1,0);
          goto LAB__text__00477189;
        }
      }
    }
    local_28 = FUN__text__00476680(param_1,1);
    switch(local_28) {
    case 0:
      break;
    case 1:
      iVar2 = FUN__text__004697f0(param_1);
      if (iVar2 == 0) {
        FUN__text__00475270(param_1,0xf);
      }
      else {
        FUN__text__00475270(param_1,2);
      }
      break;
    case 2:
      iVar2 = FUN__text__004697f0(param_1);
      if (iVar2 == 0) {
        FUN__text__00475270(param_1,0xf);
      }
      else {
        FUN__text__00475270(param_1,2);
      }
      break;
    case 3:
    case 4:
      iVar2 = FUN__text__004697f0(param_1);
      if (iVar2 == 0) {
        FUN__text__00475270(param_1,0xf);
      }
      else {
        FUN__text__00475270(param_1,2);
      }
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e04 + 0x67,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
LAB__text__00477189:
  local_8 = 0x477196;
  FUN__text__0056ce80();
  return;
}

