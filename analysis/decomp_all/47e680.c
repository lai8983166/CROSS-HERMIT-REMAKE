
void FUN__text__0047e680(int param_1)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_98 [16];
  undefined4 local_58;
  char local_54;
  int local_50;
  int local_4c;
  int local_48;
  undefined2 local_44;
  undefined2 local_40;
  undefined2 local_3c;
  undefined2 local_38;
  int local_34;
  short local_30;
  short local_2c;
  short local_28;
  short local_24;
  int local_20;
  int local_1c;
  undefined4 local_18;
  char *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar6 = local_98;
  for (iVar3 = 0x25; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_c = param_1 + 0x290;
  local_14 = (char *)(param_1 + 0x293);
  local_10 = FUN__text__0047a8e0(param_1);
  local_4c = (int)*local_14;
  switch(local_4c) {
  case 0:
    *(undefined1 *)(param_1 + 0x294) = 0;
    *(undefined2 *)(param_1 + 0x4e0) = 0;
    iVar3 = FUN__text__00469ad0(param_1);
    if (iVar3 != 0) {
      FUN__text__00475270(param_1,0x13);
      break;
    }
    if ((*(short *)(param_1 + 0x4ee) == -1) &&
       (iVar3 = FUN__text__00424f80("wk->target != -1",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e78 + 0x23,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_34 = local_8 + 0x80aec + *(short *)(param_1 + 0x4ee) * 0x520;
    iVar3 = FUN__text__004690a0(local_34);
    if ((iVar3 != 0) || (iVar3 = FUN__text__004695d0(local_34), iVar3 != 0)) {
      *(undefined2 *)(param_1 + 0x4ee) = 0xffff;
      *(undefined2 *)(param_1 + 0x4f2) = 0xffff;
      FUN__text__00475270(param_1,0xf);
      break;
    }
    local_24 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                            (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_28 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                            (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    local_2c = (short)((int)((*(int *)(local_34 + 0x2ec) >> 0x10) +
                            (*(int *)(local_34 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_30 = (short)((int)((*(int *)(local_34 + 0x2f0) >> 0x10) +
                            (*(int *)(local_34 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    local_18 = FUN__text__00470620((int)local_24,(int)local_28,(int)local_2c,(int)local_30);
    local_18 = FUN__text__004706d0(local_18);
    local_1c = FUN__text__00470720(local_18);
    iVar5 = local_1c * 3;
    iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e78 + 0x39);
    local_1c = (int)(char)(&DAT_00618dc8)[iVar3 % 3 + iVar5];
    local_38 = (undefined2)
               ((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                     (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    uVar2 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU))
            >> 4;
    local_3c = (undefined2)uVar2;
    local_50 = (int)*(char *)(local_10 + 0x24);
    switch(local_50) {
    case 0:
      local_20 = FUN__text__00438f70(CONCAT22((short)((uint)(param_1 + 0x2f4) >> 0x10),local_38),
                                     uVar2 & 0xffff,local_1c,param_1 + 0x2f4,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),1,10);
      uVar4 = extraout_var;
      break;
    case 1:
      local_20 = FUN__text__00438f70(CONCAT22((short)((uint)(param_1 + 0x2f4) >> 0x10),local_38),
                                     uVar2 & 0xffff,local_1c,param_1 + 0x2f4,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),1,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x2c));
      uVar4 = extraout_var_00;
      break;
    case 2:
      local_20 = FUN__text__00438f70(CONCAT22((short)((uint)(param_1 + 0x2f4) >> 0x10),local_38),
                                     uVar2 & 0xffff,local_1c,param_1 + 0x2f4,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),1,
                                     (uint)*(byte *)(*(int *)(param_1 + 600) + 0x2c) << 1);
      uVar4 = extraout_var_01;
      break;
    case 3:
      local_20 = FUN__text__00438f70(CONCAT22((short)((uint)(param_1 + 0x2f4) >> 0x10),local_38),
                                     uVar2 & 0xffff,local_1c,param_1 + 0x2f4,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),1,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x37));
      uVar4 = extraout_var_02;
      break;
    case 4:
      local_20 = FUN__text__00438f70(CONCAT22((short)((uint)(param_1 + 0x2f4) >> 0x10),local_38),
                                     uVar2 & 0xffff,local_1c,param_1 + 0x2f4,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),1,
                                     (uint)*(byte *)(*(int *)(param_1 + 600) + 0x37) << 1);
      uVar4 = extraout_var_03;
      break;
    case 5:
      local_20 = FUN__text__00438ba0(CONCAT22((short)((uint)(param_1 + 0x2f4) >> 0x10),local_38),
                                     uVar2 & 0xffff,local_1c,param_1 + 0x2f4,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),1);
      uVar4 = extraout_var_04;
      break;
    default:
      iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e78 + 0x53,0);
      uVar4 = extraout_var_05;
      if (iVar3 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    if (local_20 == 0) {
      FUN__text__0046bcc0(param_1,1);
      iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e78 + 0x62);
      *(short *)(param_1 + 10) = (short)(iVar3 % 0x78);
      *local_14 = *local_14 + '\x01';
      *(undefined2 *)(param_1 + 10) = 0;
      break;
    }
    local_40 = *(undefined2 *)(param_1 + 0x30c);
    local_44 = *(undefined2 *)(param_1 + 0x30e);
    FUN__text__0047d190(param_1,local_40,CONCAT22(uVar4,local_44));
    *local_14 = '\x02';
  case 2:
    iVar3 = FUN__text__004698a0(param_1);
    if ((iVar3 != 0) && (local_48 = FUN__text__0047a920(param_1), local_48 != 0)) {
      local_10 = FUN__text__0047a8e0(param_1);
      local_54 = *(char *)(local_10 + 0x12);
      if (local_54 == '\x02') {
        *(undefined2 *)(param_1 + 0x4ee) = *(undefined2 *)(local_48 + 2);
        FUN__text__00475270(param_1,0x1d);
        FUN__text__00437d90(param_1,0);
      }
      else if (local_54 == '\x03') {
        iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e78 + 0xa0,0);
        if (iVar3 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      else if (local_54 == '\x04') {
        FUN__text__00475270(param_1,6);
        FUN__text__00437d90(param_1,0);
        break;
      }
    }
    local_58 = FUN__text__00476680(param_1,1);
    switch(local_58) {
    case 0:
      break;
    case 1:
      iVar3 = FUN__text__004697f0(param_1);
      if (iVar3 == 0) {
        *local_14 = '\x03';
      }
      else {
        *local_14 = '\x03';
      }
      break;
    case 2:
      iVar3 = FUN__text__004697f0(param_1);
      if (iVar3 == 0) {
        *local_14 = '\x03';
      }
      else {
        *local_14 = '\x03';
      }
      break;
    case 3:
    case 4:
      iVar3 = FUN__text__004697f0(param_1);
      if (iVar3 == 0) {
        *local_14 = '\x03';
      }
      else {
        *local_14 = '\x03';
      }
      break;
    default:
      iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e78 + 0xbb,0);
      if (iVar3 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    break;
  case 1:
    if (0x3c < *(short *)(param_1 + 10)) {
      *local_14 = '\x03';
    }
    break;
  case 3:
    *(undefined2 *)(param_1 + 0x4ee) = 0xffff;
    *(undefined2 *)(param_1 + 0x4f2) = 0xffff;
    FUN__text__00475270(param_1,0xf);
  }
  local_8 = 0x47ed4b;
  FUN__text__0056ce80();
  return;
}

