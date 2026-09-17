
void FUN__text__004771d0(int param_1)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined2 extraout_var;
  undefined4 *puVar4;
  undefined4 local_84 [16];
  undefined4 local_44;
  int local_40;
  int local_3c;
  char local_38;
  int local_34;
  int local_30;
  undefined2 local_2c;
  undefined2 local_28;
  undefined2 local_24;
  undefined2 local_20;
  char local_1c;
  int local_18;
  char *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_84;
  for (iVar3 = 0x20; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_1 + 0x290;
  local_14 = (char *)(param_1 + 0x293);
  local_38 = *local_14;
  if (local_38 == '\0') {
    *(undefined1 *)(param_1 + 0x294) = 0;
    *(undefined2 *)(param_1 + 0x4e0) = 0;
    iVar3 = FUN__text__00469ad0(param_1);
    if (iVar3 != 0) {
      FUN__text__00475270(param_1,0x13);
      goto LAB__text__00477661;
    }
    local_3c = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                   DAT_00618e08 + 0x14);
    local_3c = local_3c % 3;
    if (local_3c == 1) {
      local_1c = (&DAT_00618cd4)[*(char *)(param_1 + 0x28a)];
    }
    else if (local_3c == 2) {
      local_1c = (&DAT_00618ce0)[*(char *)(param_1 + 0x28a)];
    }
    else {
      local_1c = (&DAT_00618cc8)[*(char *)(param_1 + 0x28a)];
    }
    local_20 = (undefined2)
               ((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                     (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    uVar2 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU))
            >> 4;
    local_24 = (undefined2)uVar2;
    local_18 = local_3c;
    iVar3 = FUN__text__00438ba0(CONCAT22((short)((uint)(param_1 + 0x2f4) >> 0x10),local_20),
                                uVar2 & 0xffff,(int)local_1c,param_1 + 0x2f4,
                                *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),1);
    if (iVar3 == 0) {
      FUN__text__0046bcc0(param_1,1);
      iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e08 + 0x2b);
      *(short *)(param_1 + 10) = (short)(iVar3 % 0x78);
      *local_14 = *local_14 + '\x01';
      *(undefined2 *)(param_1 + 10) = 0;
      goto LAB__text__00477661;
    }
    local_28 = *(undefined2 *)(param_1 + 0x30c);
    local_2c = *(undefined2 *)(param_1 + 0x30e);
    FUN__text__0047d190(param_1,local_28,CONCAT22(extraout_var,local_2c));
    *local_14 = '\x02';
  }
  else {
    if (local_38 == '\x01') {
      if (0xb4 < *(short *)(param_1 + 10)) {
        *local_14 = '\0';
      }
      goto LAB__text__00477661;
    }
    if (local_38 != '\x02') goto LAB__text__00477661;
  }
  iVar3 = FUN__text__004698a0(param_1);
  if (iVar3 != 0) {
    iVar3 = FUN__text__0047b790(param_1);
    if ((iVar3 != 0) && (iVar3 = FUN__text__0047b920(param_1,param_1 + 0x4fc), iVar3 != 0))
    goto LAB__text__00477661;
    iVar3 = FUN__text__0047cc90(param_1);
    if (iVar3 != 0) {
      local_30 = local_8 + 0x80aec + *(short *)(param_1 + 0x4fa) * 0x520;
      iVar3 = FUN__text__0047ce70(param_1,local_30);
      if (iVar3 != 0) {
        FUN__text__00437d90(param_1,0);
        goto LAB__text__00477661;
      }
    }
    local_34 = FUN__text__0047a920(param_1);
    if (local_34 != 0) {
      local_10 = FUN__text__0047a8e0(param_1);
      local_40 = (int)*(char *)(local_10 + 0x12);
      switch(local_40) {
      case 0:
        iVar3 = FUN__text__0047c580(param_1,local_34);
        if (iVar3 != 0) {
          FUN__text__00475270(param_1,6);
          FUN__text__00437d90(param_1,0);
          goto LAB__text__00477661;
        }
        break;
      case 2:
        *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(local_34 + 2);
        FUN__text__00475270(param_1,0x1d);
        FUN__text__00437d90(param_1,0);
        break;
      case 3:
        iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e08 + 0x65,0);
        if (iVar3 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        break;
      case 4:
        FUN__text__00475270(param_1,6);
        FUN__text__00437d90(param_1,0);
        goto LAB__text__00477661;
      }
    }
  }
  local_44 = FUN__text__00476680(param_1,1);
  switch(local_44) {
  case 0:
    break;
  case 1:
    iVar3 = FUN__text__004697f0(param_1);
    if (iVar3 == 0) {
      *local_14 = '\0';
    }
    else {
      *local_14 = '\0';
    }
    break;
  case 2:
    iVar3 = FUN__text__004697f0(param_1);
    if (iVar3 == 0) {
      *local_14 = '\0';
    }
    else {
      *local_14 = '\0';
    }
    break;
  case 3:
  case 4:
    iVar3 = FUN__text__004697f0(param_1);
    if (iVar3 == 0) {
      *local_14 = '\0';
    }
    else {
      *local_14 = '\0';
    }
    break;
  default:
    iVar3 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e08 + 0x80,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
LAB__text__00477661:
  local_8 = 0x477671;
  FUN__text__0056ce80();
  return;
}

