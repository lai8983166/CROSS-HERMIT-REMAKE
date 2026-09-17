
void FUN__text__004776a0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  char local_20;
  int local_1c;
  char *local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = param_1 + 0x290;
  local_18 = (char *)(param_1 + 0x293);
  local_20 = *local_18;
  if (local_20 == '\0') {
    FUN__text__0046bcc0(param_1,1);
    *local_18 = *local_18 + '\x01';
  }
  else if ((local_20 == '\x01') && (0xb3 < *(short *)(param_1 + 10))) {
    FUN__text__0046bcc0(param_1,0x18);
    *local_18 = *local_18 + '\x01';
  }
  if (*local_18 != '\0') {
    iVar2 = FUN__text__00468d80(param_1);
    if ((iVar2 != 0) && (*(char *)(*(int *)(param_1 + 600) + 0x9f) == '\x03')) {
      FUN__text__00475270(param_1,0xf);
      goto LAB__text__0047794c;
    }
    iVar2 = FUN__text__0047b790(param_1);
    if ((iVar2 != 0) && (iVar2 = FUN__text__0047b920(param_1,param_1 + 0x4fc), iVar2 != 0))
    goto LAB__text__0047794c;
    iVar2 = FUN__text__0047cc90(param_1);
    if (iVar2 != 0) {
      local_1c = local_8 + 0x80aec + *(short *)(param_1 + 0x4fa) * 0x520;
      iVar2 = FUN__text__0047ce70(param_1,local_1c);
      if (iVar2 != 0) goto LAB__text__0047794c;
    }
    iVar2 = FUN__text__00480480(param_1);
    if (iVar2 != 0) {
      iVar2 = FUN__text__00468d80(param_1);
      if ((iVar2 != 0) &&
         (iVar2 = FUN__text__00424f80("IsUwHuman(wk)==0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e0c + 0x52,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      iVar2 = FUN__text__00469ad0(param_1);
      if ((iVar2 != 0) &&
         (iVar2 = FUN__text__00424f80("IsUwBaseUnit(wk)==0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618e0c + 0x53,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      FUN__text__00475270(param_1,0x18);
      goto LAB__text__0047794c;
    }
    local_c = FUN__text__0047a920(param_1);
    if (local_c != 0) {
      local_14 = FUN__text__0047a8e0(param_1);
      local_24 = (int)*(char *)(local_14 + 0x12);
      switch(local_24) {
      case 0:
        iVar2 = FUN__text__0047c580(param_1,local_c);
        if (iVar2 != 0) {
          FUN__text__00475270(param_1,6);
          goto LAB__text__0047794c;
        }
        break;
      case 2:
        *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(local_c + 2);
        FUN__text__00475270(param_1,0x1d);
        break;
      case 3:
        iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e0c + 0x70,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        break;
      case 4:
        FUN__text__00475270(param_1,6);
        goto LAB__text__0047794c;
      }
    }
  }
LAB__text__0047794c:
  local_8 = 0x477959;
  FUN__text__0056ce80();
  return;
}

