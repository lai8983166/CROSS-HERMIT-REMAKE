
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int __fastcall FUN__text__0053d35b(int param_1)

{
  int *piVar1;
  short sVar2;
  float fVar3;
  float fVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  float fVar8;
  float fVar9;
  float *pfVar10;
  float fVar11;
  undefined4 *puVar12;
  undefined1 local_2ec [12];
  undefined4 local_2e0;
  float local_2dc;
  float local_2d8;
  undefined4 local_2d4;
  undefined4 local_2d0;
  float local_2cc;
  undefined4 local_2c8;
  undefined4 local_2c4;
  float local_2c0;
  float local_2bc [3];
  undefined1 local_2b0 [8];
  float local_2a8;
  undefined4 local_2a4;
  undefined4 local_2a0;
  undefined4 local_29c;
  float local_298;
  float local_294;
  float local_290;
  undefined4 local_28c;
  undefined4 local_288;
  undefined4 local_284;
  float local_280;
  float local_27c;
  float local_278;
  float local_274;
  float local_270;
  undefined4 local_26c;
  float local_268;
  float local_264;
  float local_260;
  undefined4 local_25c;
  float local_258;
  float local_254;
  float local_250;
  float local_24c;
  undefined4 local_244;
  undefined4 local_240;
  undefined4 local_23c;
  float local_238 [10];
  undefined4 local_210;
  undefined4 local_20c;
  undefined4 local_208;
  float local_204;
  undefined4 local_200;
  float local_1fc;
  float local_1f8;
  undefined4 local_1f4;
  undefined4 local_1f0;
  undefined4 local_1ec;
  float local_1e8;
  undefined4 local_1e4;
  float local_1e0;
  undefined4 local_1dc;
  undefined4 local_1d8;
  undefined4 local_1d4;
  undefined4 local_1d0;
  undefined4 local_1cc;
  float local_1c8;
  undefined4 local_1c4;
  float local_1c0 [6];
  float local_1a8;
  undefined4 local_1a4;
  undefined4 local_1a0;
  float local_19c;
  undefined4 local_198;
  float local_194;
  float local_190;
  float local_18c;
  undefined4 local_188;
  float local_184;
  undefined4 local_180;
  undefined4 local_17c;
  float local_178;
  undefined4 local_174;
  undefined4 local_170;
  undefined4 local_16c;
  float local_168;
  undefined4 local_164;
  float local_160;
  undefined4 local_15c;
  float local_158;
  float local_154 [7];
  float local_138;
  float local_134;
  float local_130;
  float local_12c;
  undefined4 local_128;
  undefined4 local_124;
  float local_120;
  undefined4 local_11c;
  undefined4 local_118;
  undefined4 local_114;
  undefined4 local_110;
  uint local_10c;
  float local_108;
  float local_104;
  undefined4 local_100;
  undefined4 local_fc;
  undefined4 local_f8;
  undefined4 local_f4;
  undefined4 local_f0;
  undefined4 local_ec;
  undefined4 local_e8;
  undefined4 local_e4;
  undefined4 local_e0;
  undefined4 local_dc;
  float local_d8;
  float local_d4;
  float local_d0;
  float local_cc;
  float local_c8;
  float local_c4;
  float local_c0;
  float local_bc;
  float local_b8;
  float local_b4;
  uint local_b0;
  float local_ac;
  float local_a8;
  float local_a4;
  float local_a0;
  float local_9c;
  float local_98;
  float local_94;
  float local_90;
  float local_8c;
  float local_88;
  float local_84;
  float local_80;
  float local_7c;
  float local_78;
  float local_74;
  float local_70;
  float local_6c;
  uint local_68;
  float local_64;
  float local_60;
  uint local_5c;
  int local_58;
  float local_54;
  float local_50;
  float local_4c;
  int local_48;
  float local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  uint local_2c;
  int local_28;
  int local_24;
  uint local_20;
  float local_1c;
  float local_18;
  short *local_14;
  float *local_10;
  float local_c;
  float local_8;
  
  local_24 = *(int *)(param_1 + 0x460);
  local_20 = 0;
  local_10c = (local_24 != 2) + 1;
  local_58 = param_1;
  fVar3 = _DAT_005d0a5c;
  if (local_10c != 0) {
    do {
      local_10 = (float *)0x0;
      local_14 = (short *)0x0;
      local_2c = 0;
      do {
        local_28 = 0;
        local_48 = 0;
        local_5c = 0;
        do {
          fVar9 = _DAT_005d0a54;
          if (local_2c != 0) {
            iVar5 = (local_20 + local_24 * 2) * 0x68;
            *(int *)(local_5c * 0x10 + iVar5 + 0x58 + local_58) = local_28;
            *(int *)((local_5c + 6) * 0x10 + iVar5 + local_58) = local_48;
          }
          if (local_5c == 0) {
            local_1d8 = 0x3f800000;
            local_1d4 = 0;
            local_1d0 = 0x3f800000;
            local_44 = 1.0;
            local_1f0 = 0x3f800000;
            local_40 = 0.0;
            local_1ec = 0;
            local_1e8 = fVar3;
            local_3c = 1.0;
            local_208 = 0x3f800000;
            local_204 = fVar3;
            local_80 = 1.0;
            local_200 = 0;
            local_238[6] = 1.0;
            local_238[7] = 1.0;
            local_238[8] = 0.0;
            local_38 = 1.0;
            local_238[0] = 1.0;
            local_238[1] = 0.0;
            local_238[2] = 0.0;
            local_30 = 0.0;
            local_70 = 1.0;
            local_6c = 0.0;
            pfVar10 = local_238;
            local_78 = fVar3;
            local_34 = fVar3;
LAB__text__0053d84a:
            local_a8 = *pfVar10;
            local_a4 = pfVar10[1];
            local_a0 = pfVar10[2];
            local_7c = local_40;
            local_74 = local_38;
          }
          else {
            if (local_5c == 1) {
              local_160 = fVar3;
              local_15c = 0;
              local_158 = fVar3;
              local_178 = fVar3;
              local_40 = 0.0;
              local_174 = 0;
              local_170 = 0x3f800000;
              local_190 = fVar3;
              local_18c = fVar3;
              local_188 = 0;
              local_1a8 = fVar3;
              local_1a4 = 0x3f800000;
              local_78 = 1.0;
              local_1a0 = 0;
              local_1c0[0] = fVar3;
              local_1c0[1] = 0.0;
              local_1c0[2] = 0.0;
              local_30 = 0.0;
              local_70 = 1.0;
              local_6c = 0.0;
              pfVar10 = local_1c0;
              local_80 = fVar3;
              local_44 = fVar3;
              local_3c = fVar3;
              local_38 = fVar3;
              local_34 = fVar3;
              goto LAB__text__0053d84a;
            }
            if (local_5c == 2) {
              local_28c = 0x3f800000;
              local_288 = 0x3f800000;
              local_284 = 0;
              local_238[9] = fVar3;
              local_44 = 1.0;
              local_40 = 1.0;
              local_210 = 0x3f800000;
              local_20c = 0;
              local_3c = 0.0;
              local_2d4 = 0;
              local_2d0 = 0x3f800000;
              local_238[3] = 0.0;
              local_78 = 0.0;
              local_238[4] = 1.0;
              local_238[5] = 1.0;
              local_38 = 0.0;
              local_154[0] = 0.0;
              local_154[1] = 1.0;
              local_34 = 1.0;
              local_154[2] = 0.0;
              local_70 = 1.0;
              local_6c = 1.0;
              pfVar10 = local_154;
              local_2cc = fVar3;
              local_80 = fVar3;
              local_30 = fVar3;
              goto LAB__text__0053d84a;
            }
            if (local_5c == 3) {
              local_1cc = 0x3f800000;
              local_1c8 = fVar3;
              local_1c4 = 0;
              local_274 = fVar3;
              local_44 = 1.0;
              local_270 = fVar3;
              local_26c = 0;
              local_3c = 0.0;
              local_1e4 = 0;
              local_1e0 = fVar3;
              local_1dc = 0x3f800000;
              local_2e0 = 0;
              local_78 = 0.0;
              local_1fc = 0.0;
              local_1f8 = fVar3;
              local_38 = 0.0;
              local_1f4 = 0;
              local_30 = 1.0;
              pfVar10 = &local_1fc;
              local_2dc = fVar3;
              local_2d8 = fVar3;
              local_80 = fVar3;
              local_70 = fVar3;
              local_6c = fVar3;
              local_40 = fVar3;
              local_34 = fVar3;
              goto LAB__text__0053d84a;
            }
            if (local_5c == 4) {
              local_2c8 = 0x3f800000;
              local_2c4 = 0;
              local_19c = fVar3;
              local_44 = 1.0;
              local_40 = 0.0;
              local_198 = 0;
              local_194 = fVar3;
              local_25c = 0;
              local_258 = fVar3;
              local_254 = fVar3;
              local_1c0[3] = 0.0;
              local_1c0[4] = 1.0;
              local_1c0[5] = fVar3;
              local_2bc[0] = 0.0;
              local_38 = 0.0;
              local_2bc[1] = 0.0;
              local_2bc[2] = fVar3;
              local_70 = 1.0;
              pfVar10 = local_2bc;
              local_2c0 = fVar3;
              local_80 = fVar3;
              local_78 = fVar3;
              local_6c = fVar3;
              local_3c = fVar3;
              local_34 = fVar3;
              local_30 = fVar3;
              goto LAB__text__0053d84a;
            }
            if (local_5c == 5) {
              local_184 = fVar3;
              local_180 = 0;
              local_17c = 0x3f800000;
              local_2a4 = 0x3f800000;
              local_40 = 0.0;
              local_2a0 = 0;
              local_3c = 1.0;
              local_29c = 0x3f800000;
              local_16c = 0;
              local_80 = 1.0;
              local_168 = fVar3;
              local_164 = 0x3f800000;
              local_244 = 0;
              local_78 = 1.0;
              local_240 = 0x3f800000;
              local_23c = 0x3f800000;
              local_38 = 0.0;
              local_154[3] = 0.0;
              local_154[4] = 0.0;
              local_154[5] = 1.0;
              local_30 = 1.0;
              local_70 = 1.0;
              local_6c = 1.0;
              pfVar10 = local_154 + 3;
              local_44 = fVar3;
              local_34 = fVar3;
              goto LAB__text__0053d84a;
            }
          }
          if (local_24 == 2) {
            local_b0 = (uint)(local_5c == 4);
            local_18 = 0.0;
            local_1c = 0.0;
            local_8 = 2.24208e-44;
            local_c = 2.24208e-44;
LAB__text__0053da2a:
            if ((local_1c != local_c) && (local_18 != local_8)) {
              if (local_b0 == 0) {
                if (local_2c != 0) {
                  fVar9 = local_1c;
                  if ((uint)local_1c <= (uint)local_c) {
                    local_98 = local_74 - local_38;
                    local_90 = local_70 - local_34;
                    local_84 = local_6c - local_30;
                    fVar8 = local_1c;
                    do {
                      local_104 = (float)(int)fVar8;
                      if ((int)fVar8 < 0) {
                        local_104 = local_104 + _DAT_005d0a44;
                      }
                      local_104 = local_104 * _DAT_005d0e90;
                      local_154[6] = local_98 * local_104 + local_38;
                      local_138 = local_90 * local_104 + local_34;
                      local_134 = local_84 * local_104 + local_30;
                      local_4c = fVar8;
                      if ((uint)local_18 <= (uint)local_8) {
                        local_94 = local_80 - local_44;
                        local_9c = local_7c - local_40;
                        local_ac = local_78 - local_3c;
                        local_4c = 1.0 - local_104;
                        fVar9 = local_18;
                        do {
                          local_108 = (float)(int)fVar9;
                          if ((int)fVar9 < 0) {
                            local_108 = local_108 + _DAT_005d0a44;
                          }
                          local_108 = local_108 * _DAT_005d0e90;
                          local_298 = (local_94 * local_108 + local_44 + local_154[6]) - local_a8;
                          local_294 = (local_9c * local_108 + local_40 + local_138) - local_a4;
                          local_290 = (local_ac * local_108 + local_3c + local_134) - local_a0;
                          local_c0 = fVar9;
                          thunk_FUN__text__00554de0(local_2b0,&local_298);
                          FUN__text__0053d261(local_10,local_2b0,local_24,local_20);
                          local_10[3] = -NAN;
                          local_10[4] = 1.0 - local_108;
                          local_10[5] = local_4c;
                          if (((local_2a8 < _DAT_005d0a54) && (local_20 == 0)) ||
                             ((_DAT_005d0a54 < local_2a8 && (local_20 == 1)))) {
                            if (local_24 == 4) {
                              local_10[3] = 2.3509886e-38;
                            }
                            fVar3 = _DAT_005d0e20;
                            if (local_24 == 3) {
                              *local_10 = *local_10 * _DAT_005d0e20;
                              local_10[1] = local_10[1] * fVar3;
                              local_10[2] = local_10[2] * fVar3;
                            }
                          }
                          local_10 = local_10 + 6;
                          fVar9 = (float)((int)fVar9 + 1);
                          fVar3 = _DAT_005d0a5c;
                        } while ((uint)fVar9 <= (uint)local_8);
                      }
                      fVar8 = (float)((int)fVar8 + 1);
                      fVar9 = local_1c;
                    } while ((uint)fVar8 <= (uint)local_c);
                  }
                  for (; (uint)fVar9 < (uint)local_c; fVar9 = (float)((int)fVar9 + 1)) {
                    if ((uint)local_18 < (uint)local_8) {
                      sVar2 = SUB42(local_18,0);
                      fVar8 = local_18;
                      do {
                        *local_14 = SUB42(fVar8,0) +
                                    (((SUB42(local_8,0) - sVar2) + 1) *
                                     (SUB42(fVar9,0) - SUB42(local_1c,0)) - sVar2) + (short)local_28
                        ;
                        local_14[1] = (*local_14 - sVar2) + 1 + SUB42(local_8,0);
                        local_14[2] = *local_14 + 1;
                        local_14[3] = local_14[2];
                        local_14[4] = local_14[1];
                        local_14[5] = local_14[1] + 1;
                        local_14 = local_14 + 6;
                        fVar8 = (float)((int)fVar8 + 1);
                      } while ((uint)fVar8 < (uint)local_8);
                    }
                  }
                }
                local_48 = local_48 +
                           ((int)local_c * 6 + (int)local_1c * -6) * ((int)local_8 - (int)local_18);
                local_28 = local_28 +
                           (((int)local_c - (int)local_1c) + 1) *
                           (((int)local_8 - (int)local_18) + 1);
              }
              else if (local_b0 == 1) {
                if (local_2c != 0) {
                  local_8 = (float)((uint)local_8 >> 1);
                  local_94 = local_80 - local_44;
                  local_68 = 0;
                  local_9c = local_7c - local_40;
                  local_ac = local_78 - local_3c;
                  local_98 = local_74 - local_38;
                  local_90 = local_70 - local_34;
                  local_84 = local_6c - local_30;
                  do {
                    if (local_68 == 0) {
                      local_114 = 0;
                      local_110 = 0;
                      local_64 = 0.0;
                      local_f8 = 0x3f800000;
                      local_60 = 0.0;
                      local_f4 = 0;
                      local_8c = 1.0;
                      local_88 = 0.0;
                    }
                    else if (local_68 == 1) {
                      local_11c = 0x3f800000;
                      local_118 = 0;
                      local_64 = 1.0;
                      local_128 = 0x3f800000;
                      local_60 = 0.0;
                      local_124 = 0x3f800000;
                      local_8c = 1.0;
                      local_88 = 1.0;
                    }
                    else if (local_68 == 2) {
                      local_100 = 0x3f800000;
                      local_fc = 0x3f800000;
                      local_64 = 1.0;
                      local_e0 = 0;
                      local_60 = 1.0;
                      local_dc = 0x3f800000;
                      local_8c = 0.0;
                      local_88 = 1.0;
                    }
                    else if (local_68 == 3) {
                      local_e8 = 0;
                      local_e4 = 0x3f800000;
                      local_64 = 0.0;
                      local_f0 = 0;
                      local_60 = 1.0;
                      local_ec = 0;
                      local_8c = 0.0;
                      local_88 = 0.0;
                    }
                    fVar9 = 0.0;
                    local_120 = local_8c - local_64;
                    local_c0 = local_88 - local_60;
                    do {
                      fVar8 = (float)(int)fVar9;
                      if ((int)fVar9 < 0) {
                        fVar8 = fVar8 + _DAT_005d0a44;
                      }
                      fVar11 = 0.0;
                      local_54 = local_120 * fVar8 * _DAT_005d0e90 + local_64;
                      local_50 = local_c0 * fVar8 * _DAT_005d0e90 + local_60;
                      local_4c = fVar9;
                      if (local_8 != 0.0) {
                        local_4c = (float)(int)((int)local_8 - 1U);
                        if ((int)((int)local_8 - 1U) < 0) {
                          local_4c = local_4c + _DAT_005d0a44;
                        }
                        local_b8 = _DAT_005d0a3c - local_54;
                        local_bc = _DAT_005d0a3c - local_50;
                        do {
                          fVar3 = (float)(int)fVar11;
                          if ((int)fVar11 < 0) {
                            fVar3 = fVar3 + _DAT_005d0a44;
                          }
                          fVar3 = fVar3 / local_4c;
                          local_b4 = _DAT_005d1204 * fVar3;
                          fVar4 = local_b4 * local_b8 + local_54;
                          fVar8 = local_b4 * local_bc + local_50;
                          local_cc = local_94 * fVar4 + local_44;
                          local_c8 = local_9c * fVar4 + local_40;
                          local_c4 = local_ac * fVar4 + local_3c;
                          local_d8 = local_98 * fVar8 + local_38;
                          local_d4 = local_90 * fVar8 + local_34;
                          local_130 = fVar3 * local_b8 + local_54;
                          local_12c = fVar3 * local_bc + local_50;
                          local_250 = local_d8 + local_cc;
                          local_24c = local_d4 + local_c8;
                          local_268 = local_250 - local_a8;
                          local_264 = local_24c - local_a4;
                          local_260 = (local_84 * fVar8 + local_30 + local_c4) - local_a0;
                          thunk_FUN__text__00554de0(local_2ec,&local_268);
                          FUN__text__0053d261(local_10,local_2ec,local_24,local_20);
                          local_10[3] = -NAN;
                          local_10[4] = 1.0 - local_130;
                          local_10[5] = 1.0 - local_12c;
                          local_10 = local_10 + 6;
                          fVar11 = (float)((int)fVar11 + 1);
                          fVar3 = _DAT_005d0a5c;
                        } while ((uint)fVar11 < (uint)local_8);
                      }
                      local_c4 = local_ac * local_54 + local_3c;
                      local_d4 = local_90 * local_50 + local_34;
                      local_d0 = local_84 * local_50 + local_30;
                      local_280 = (local_98 * local_50 + local_38 + local_94 * local_54 + local_44)
                                  - local_a8;
                      local_27c = (local_d4 + local_9c * local_54 + local_40) - local_a4;
                      local_278 = (local_d0 + local_c4) - local_a0;
                      *local_10 = local_280;
                      fVar8 = _DAT_005d0a3c;
                      local_10[1] = local_27c;
                      local_10[2] = local_278;
                      local_10[3] = -NAN;
                      local_10[4] = fVar8;
                      local_10[5] = _DAT_005d0a3c;
                      local_10 = local_10 + 6;
                      fVar9 = (float)((int)fVar9 + 1);
                    } while ((uint)fVar9 <= (uint)local_c);
                    fVar9 = 0.0;
                    if (local_c != 0.0) {
                      do {
                        fVar8 = 0.0;
                        if (local_8 != 0.0) {
                          do {
                            *local_14 = SUB42(fVar8,0) +
                                        ((SUB42(local_c,0) + 1) * (short)local_68 + SUB42(fVar9,0))
                                        * (SUB42(local_8,0) + 1) + (short)local_28;
                            local_14[1] = *local_14 + SUB42(local_8,0) + 1;
                            local_14[2] = *local_14 + 1;
                            local_14[3] = local_14[2];
                            local_14[4] = local_14[1];
                            local_14[5] = local_14[1] + 1;
                            local_14 = local_14 + 6;
                            fVar8 = (float)((int)fVar8 + 1);
                          } while ((uint)fVar8 < (uint)local_8);
                        }
                        fVar9 = (float)((int)fVar9 + 1);
                      } while ((uint)fVar9 < (uint)local_c);
                    }
                    local_68 = local_68 + 1;
                  } while (local_68 < 4);
                }
                local_28 = local_28 + ((int)local_c * 4 + 4) * ((int)local_8 + 1);
                local_48 = local_48 + (int)local_c * (int)local_8 * 0x18;
              }
            }
          }
          else {
            if (local_24 == 3) {
              local_b0 = 0;
              if (local_20 == 0) {
                local_18 = 9.80909e-45;
                if (fVar9 <= local_3c) {
                  local_18 = 0.0;
                }
                local_8 = 1.26117e-44;
                if (fVar9 <= local_78) {
                  local_8 = 2.24208e-44;
                }
                local_1c = 9.80909e-45;
                if (fVar9 <= local_30) {
                  local_1c = 0.0;
                }
                if (fVar9 <= local_6c) goto LAB__text__0053d9aa;
LAB__text__0053da05:
                local_c = 1.26117e-44;
              }
              else if (local_20 == 1) {
                local_18 = 9.80909e-45;
                if (local_3c <= fVar9) {
                  local_18 = 0.0;
                }
                local_8 = 1.26117e-44;
                if (local_78 <= fVar9) {
                  local_8 = 2.24208e-44;
                }
                local_1c = 9.80909e-45;
                if (local_30 <= fVar9) {
                  local_1c = 0.0;
                }
                if (fVar9 < local_6c) goto LAB__text__0053da05;
LAB__text__0053d9aa:
                local_b0 = 0;
                local_c = 2.24208e-44;
              }
              goto LAB__text__0053da2a;
            }
            if (local_24 != 4) goto LAB__text__0053da2a;
            local_b0 = 0;
            if (local_20 == 0) {
              if (local_5c != 4) {
                local_18 = 5.60519e-45;
                if (fVar9 <= local_3c) {
                  local_18 = 0.0;
                }
                local_8 = 1.68156e-44;
                if (fVar9 <= local_78) {
                  local_8 = 2.24208e-44;
                }
                local_1c = 5.60519e-45;
                if (fVar9 <= local_30) {
                  local_1c = 0.0;
                }
                if (fVar9 <= local_6c) goto LAB__text__0053d9aa;
LAB__text__0053d93b:
                local_c = 1.68156e-44;
                goto LAB__text__0053da2a;
              }
            }
            else {
              if (local_20 != 1) goto LAB__text__0053da2a;
              if (local_5c != 5) {
                local_18 = 5.60519e-45;
                if (local_3c <= fVar9) {
                  local_18 = 0.0;
                }
                local_8 = 1.68156e-44;
                if (local_78 <= fVar9) {
                  local_8 = 2.24208e-44;
                }
                local_1c = 5.60519e-45;
                if (local_30 <= fVar9) {
                  local_1c = 0.0;
                }
                if (local_6c <= fVar9) goto LAB__text__0053d9aa;
                goto LAB__text__0053d93b;
              }
            }
            local_18 = 0.0;
            local_8 = 0.0;
            local_1c = 0.0;
            local_c = 0.0;
          }
          iVar5 = local_58;
          if (local_2c != 0) {
            iVar7 = (local_20 + local_24 * 2) * 0x68;
            iVar6 = local_5c * 0x10 + iVar7 + local_58;
            iVar7 = *(int *)((local_5c + 6) * 0x10 + iVar7 + local_58);
            *(int *)(iVar6 + 0x5c) = local_28 - *(int *)(iVar6 + 0x58);
            *(int *)(iVar6 + 100) = local_48 - iVar7;
          }
          local_5c = local_5c + 1;
        } while (local_5c < 6);
        if (local_2c == 0) {
          iVar7 = (local_20 + local_24 * 2) * 0x68 + local_58;
          puVar12 = (undefined4 *)(iVar7 + 0x50);
          iVar6 = (**(code **)(**(int **)(local_58 + 8) + 0x5c))
                            (*(int **)(local_58 + 8),local_28 * 0x18,8,0x142,1,puVar12);
          if (iVar6 < 0) {
            return iVar6;
          }
          piVar1 = (int *)*puVar12;
          iVar6 = (**(code **)(*piVar1 + 0x2c))(piVar1,0,0,&local_10,0);
          if (iVar6 < 0) {
            return iVar6;
          }
          puVar12 = (undefined4 *)(iVar7 + 0x54);
          iVar5 = (**(code **)(**(int **)(iVar5 + 8) + 0x60))
                            (*(int **)(iVar5 + 8),local_48 * 2,8,0x65,1,puVar12);
          if (iVar5 < 0) {
            return iVar5;
          }
          piVar1 = (int *)*puVar12;
          iVar5 = (**(code **)(*piVar1 + 0x2c))(piVar1,0,0,&local_14,0);
          fVar3 = _DAT_005d0a5c;
          if (iVar5 < 0) {
            return iVar5;
          }
        }
        else if (local_2c == 1) {
          iVar5 = (local_20 + local_24 * 2) * 0x68 + local_58;
          piVar1 = *(int **)(iVar5 + 0x50);
          (**(code **)(*piVar1 + 0x30))(piVar1);
          piVar1 = *(int **)(iVar5 + 0x54);
          (**(code **)(*piVar1 + 0x30))(piVar1);
          fVar3 = _DAT_005d0a5c;
        }
        local_2c = local_2c + 1;
      } while (local_2c < 2);
      local_20 = local_20 + 1;
    } while (local_20 < local_10c);
  }
  return 0;
}

