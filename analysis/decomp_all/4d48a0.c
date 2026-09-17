
void FUN__text__004d48a0(short param_1,short param_2,undefined4 param_3,short param_4)

{
  short sVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  short asStackY_300b4 [30];
  short asStackY_30078 [18];
  short asStackY_30054 [32720];
  short asStackY_200b4 [30];
  short asStackY_20078 [18];
  short asStackY_20054 [32640];
  short asStackY_10154 [4];
  short asStackY_1014c [10];
  short asStackY_10138 [10];
  short asStackY_10124 [4];
  short asStackY_1011c [10];
  short asStackY_10108 [10];
  short asStackY_100f4 [4];
  short asStackY_100ec [10];
  short asStackY_100d8 [4];
  short asStackY_100d0 [12];
  short asStackY_100b8 [14];
  short asStackY_1009c [16];
  short asStackY_1007c [16];
  short asStackY_1005c [4];
  short asStackY_10054 [16];
  short asStackY_10034 [10];
  short asStackY_10020 [32560];
  undefined4 local_1a8 [16];
  int local_168;
  int local_164;
  short local_160;
  short local_15c;
  short local_158;
  short local_154 [10];
  short local_140;
  short local_13c;
  short local_138 [4];
  short local_130;
  short local_12c;
  short local_128;
  short local_124 [4];
  short local_11c [4];
  short local_114;
  short local_110;
  short local_10c;
  short local_108 [4];
  short local_100;
  short local_fc;
  short local_f8;
  short local_f4 [4];
  short local_ec [4];
  short local_e4;
  short local_e0;
  short local_dc;
  short local_d8 [4];
  short local_d0 [4];
  short local_c8;
  short local_c4;
  short local_c0;
  short local_bc;
  short local_b8 [6];
  short local_ac;
  short local_a8;
  short local_a4;
  short local_a0;
  short local_9c [10];
  short local_88;
  short local_84;
  short local_80;
  short local_7c [10];
  short local_68;
  short local_64;
  short local_60;
  short local_5c [4];
  short local_54 [10];
  short local_40;
  short local_3c;
  short local_38;
  short local_34 [6];
  short local_28;
  short local_24;
  short local_20 [6];
  short local_14;
  undefined2 local_10;
  short local_c;
  undefined4 local_8;
  
  puVar4 = local_1a8;
  for (iVar3 = 0x69; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_10 = 0;
  local_20[4] = -1;
  local_164 = (int)param_1;
  if (0 < local_164) {
    if (local_164 < 0xd) {
      local_c = param_1;
      goto LAB__text__004d4914;
    }
    if (local_164 == 0x23) {
      local_c = 0xd;
      goto LAB__text__004d4914;
    }
  }
  local_c = -1;
LAB__text__004d4914:
  if (local_c < 1) {
    local_10 = 1;
  }
  else {
    local_168 = (int)param_2;
    switch(local_168) {
    case 0:
      local_20[2] = 0;
      local_20[3] = 1;
      local_20[0] = 0x1e;
      local_20[1] = 0x46;
      local_24 = 2;
      local_28 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_34[4] = sVar1 % 100;
      for (local_14 = 0; local_14 < local_24; local_14 = local_14 + 1) {
        local_28 = local_28 + local_20[local_14];
        if (sVar1 % 100 < local_28) {
          local_20[4] = (local_c + -1) * 0x28 + local_20[local_14 + 2];
          break;
        }
      }
      break;
    case 1:
      local_54[0] = -1;
      local_54[1] = 5;
      local_54[2] = 6;
      local_54[3] = 0xffff;
      local_54[4] = 1;
      local_54[5] = 2;
      local_54[6] = 0xffff;
      local_54[7] = 3;
      local_54[8] = 4;
      local_5c[0] = 0x14;
      local_5c[1] = 0x28;
      local_5c[2] = 0x28;
      local_60 = 3;
      local_64 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_68 = sVar1 % 100;
      local_14 = 0;
      while ((local_14 < local_60 &&
             (local_64 = local_64 + local_5c[local_14], local_64 <= sVar1 % 100))) {
        local_14 = local_14 + 1;
      }
      local_7c[8] = local_14;
      if (local_54[local_14] != -1) {
        if (param_4 < 4) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_54[local_14];
        }
        else if (param_4 < 6) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_54[(int)local_14 + (int)local_60];
        }
        else {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_54[(int)local_14 + local_60 * 2];
        }
      }
      break;
    case 2:
      local_7c[2] = 0xffff;
      local_7c[3] = 9;
      local_7c[4] = 0xffff;
      local_7c[5] = 7;
      local_7c[6] = 0xffff;
      local_7c[7] = 8;
      local_7c[0] = 0x1e;
      local_7c[1] = 0x46;
      local_80 = 2;
      local_84 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_88 = sVar1 % 100;
      local_14 = 0;
      while ((local_14 < local_80 &&
             (local_84 = local_84 + local_7c[local_14], local_84 <= sVar1 % 100))) {
        local_14 = local_14 + 1;
      }
      local_9c[8] = local_14;
      if (local_7c[local_14 + 2] != -1) {
        if (param_4 < 4) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_7c[local_14 + 2];
        }
        else if (param_4 < 6) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_7c[(int)local_14 + (int)local_80 + 2];
        }
        else {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_7c[(int)local_14 + local_80 * 2 + 2];
        }
      }
      break;
    case 3:
      local_b8[2] = 0x15;
      local_b8[3] = 0x13;
      local_b8[4] = 0x14;
      local_b8[0] = 100;
      local_bc = 1;
      local_c0 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_c4 = sVar1 % 100;
      local_14 = 0;
      while ((local_14 < local_bc &&
             (local_c0 = local_c0 + local_b8[local_14], local_c0 <= sVar1 % 100))) {
        local_14 = local_14 + 1;
      }
      local_c8 = local_14;
      if (param_4 < 4) {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_b8[local_14 + 2];
      }
      else if (param_4 < 6) {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_b8[(int)local_14 + (int)local_bc + 2];
      }
      else {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_b8[(int)local_14 + local_bc * 2 + 2];
      }
      break;
    case 4:
      local_9c[2] = 10;
      local_9c[3] = 0xd;
      local_9c[4] = 0xb;
      local_9c[5] = 0xe;
      local_9c[6] = 0xc;
      local_9c[7] = 0xf;
      local_9c[0] = 0x32;
      local_9c[1] = 0x32;
      local_a0 = 2;
      local_a4 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_a8 = sVar1 % 100;
      local_14 = 0;
      while ((local_14 < local_a0 &&
             (local_a4 = local_a4 + local_9c[local_14], local_a4 <= sVar1 % 100))) {
        local_14 = local_14 + 1;
      }
      local_ac = local_14;
      if (param_4 == 0) {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_9c[local_14 + 2];
      }
      else if (param_4 < 3) {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_9c[local_14 + 4];
      }
      else {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_9c[local_14 + 6];
      }
      break;
    case 5:
      local_34[2] = 0x10;
      local_34[3] = 0x1b;
      local_34[0] = 0x32;
      local_34[1] = 0x32;
      local_38 = 2;
      local_3c = 0;
      sVar1 = FUN__text__004d1cb0();
      local_40 = sVar1 % 100;
      for (local_14 = 0; local_14 < local_38; local_14 = local_14 + 1) {
        local_3c = local_3c + local_34[local_14];
        if (sVar1 % 100 < local_3c) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_34[local_14 + 2];
          break;
        }
      }
      break;
    case 6:
      local_d0[0] = 0x1a;
      local_d0[1] = 0x1c;
      local_d0[2] = 0x12;
      local_d8[0] = 0x1e;
      local_d8[1] = 0x28;
      local_d8[2] = 0x1e;
      local_dc = 3;
      local_e0 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_e4 = sVar1 % 100;
      for (local_14 = 0; local_14 < local_dc; local_14 = local_14 + 1) {
        local_e0 = local_e0 + local_d8[local_14];
        if (sVar1 % 100 < local_e0) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_d0[local_14];
          break;
        }
      }
      break;
    case 7:
      local_ec[0] = 0x1c;
      local_ec[1] = 0x16;
      local_ec[2] = 0x17;
      local_f4[0] = 0x28;
      local_f4[1] = 0x1e;
      local_f4[2] = 0x1e;
      local_f8 = 3;
      local_fc = 0;
      sVar1 = FUN__text__004d1cb0();
      local_100 = sVar1 % 100;
      for (local_14 = 0; local_14 < local_f8; local_14 = local_14 + 1) {
        local_fc = local_fc + local_f4[local_14];
        if (sVar1 % 100 < local_fc) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_ec[local_14];
          break;
        }
      }
      break;
    case 8:
      local_108[2] = 0x1f;
      local_108[0] = 100;
      local_10c = 1;
      local_110 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_114 = sVar1 % 100;
      for (local_14 = 0; local_14 < local_10c; local_14 = local_14 + 1) {
        local_110 = local_110 + local_108[local_14];
        if (sVar1 % 100 < local_110) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_108[local_14 + 2];
          break;
        }
      }
      break;
    case 9:
      local_11c[0] = -1;
      local_11c[1] = 0x22;
      local_11c[2] = 0x23;
      local_124[0] = 0x28;
      local_124[1] = 0x1e;
      local_124[2] = 0x1e;
      local_128 = 3;
      local_12c = 0;
      sVar1 = FUN__text__004d1cb0();
      local_130 = sVar1 % 100;
      local_14 = 0;
      while ((local_14 < local_128 &&
             (local_12c = local_12c + local_124[local_14], local_12c <= sVar1 % 100))) {
        local_14 = local_14 + 1;
      }
      if (local_11c[local_14] != -1) {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_11c[local_14];
      }
      break;
    case 10:
      local_138[2] = 0x21;
      local_138[0] = 100;
      local_13c = 1;
      local_140 = 0;
      sVar1 = FUN__text__004d1cb0();
      local_154[8] = sVar1 % 100;
      for (local_14 = 0; local_14 < local_13c; local_14 = local_14 + 1) {
        local_140 = local_140 + local_138[local_14];
        if (sVar1 % 100 < local_140) {
          local_20[4] = (local_c + -1) * 0x28 + 1 + local_138[local_14 + 2];
          break;
        }
      }
      break;
    case 0xb:
      local_154[4] = 0xffff;
      local_154[5] = 0x16;
      local_154[6] = 0x1a;
      local_154[7] = 0x1b;
      local_154[0] = 0x19;
      local_154[1] = 0x19;
      local_154[2] = 0x19;
      local_154[3] = 0x19;
      local_158 = 4;
      local_15c = 0;
      sVar1 = FUN__text__004d1cb0();
      local_160 = sVar1 % 100;
      local_14 = 0;
      while ((local_14 < local_158 &&
             (local_15c = local_15c + local_154[local_14], local_15c <= sVar1 % 100))) {
        local_14 = local_14 + 1;
      }
      if (local_154[local_14 + 4] != -1) {
        local_20[4] = (local_c + -1) * 0x28 + 1 + local_154[local_14 + 4];
      }
    }
    if (local_20[4] != -1) {
      uVar2 = FUN__text__004d1ba0((int)local_20[4],0,0x207);
      local_20[4] = (short)uVar2;
      FUN__text__004d47b0(uVar2);
    }
  }
  local_8 = 0x4d5555;
  FUN__text__0056ce80();
  return;
}

