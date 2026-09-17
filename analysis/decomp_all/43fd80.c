
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0043fd80(uint param_1,int param_2,int *param_3,int param_4)

{
  char cVar1;
  code *pcVar2;
  int iVar3;
  uint uVar4;
  undefined4 *puVar5;
  undefined4 local_17c [16];
  int local_13c;
  int local_138;
  int local_134;
  int local_130;
  int local_12c;
  int local_128;
  int local_124;
  int local_120;
  int local_11c;
  int local_118;
  int local_114;
  int local_110;
  int local_10c;
  int local_108;
  int local_104;
  int local_100;
  uint local_fc;
  undefined2 local_f8;
  undefined2 local_f6;
  undefined2 local_f4;
  undefined2 local_f2;
  int local_f0;
  int local_ec;
  int local_e8;
  int local_e4;
  int local_e0;
  int local_dc;
  int local_d8;
  int local_d4;
  uint local_d0;
  uint local_cc;
  float local_c8;
  float local_c4;
  float local_c0;
  float local_bc;
  float local_b8;
  int local_b4;
  int local_b0;
  int local_ac;
  int local_a8;
  int local_a4;
  int local_a0;
  undefined4 local_9c;
  float local_98;
  float local_94;
  float local_90;
  undefined4 local_8c;
  uint local_88;
  undefined4 local_84;
  float local_80;
  float local_7c;
  float local_78;
  float local_74;
  float local_70;
  undefined4 local_6c;
  uint local_68;
  undefined4 local_64;
  float local_60;
  float local_5c;
  float local_58;
  float local_54;
  float local_50;
  undefined4 local_4c;
  uint local_48;
  undefined4 local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  undefined4 local_2c;
  uint local_28;
  undefined4 local_24;
  float local_20;
  float local_1c;
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar5 = local_17c;
  for (iVar3 = 0x5e; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_8 = param_4;
  local_9c = 0;
  if ((*(int *)(param_4 + 0x2659c) != 0) && (param_2 != 0)) {
    local_c = param_3;
    (**(code **)(*param_3 + 200))(param_3,0x1b,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0xf,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0x130))(local_c,0x1c4);
    FUN__text__0056ce80();
    local_fc = param_1 & 0xffff;
    local_c8 = (float)local_fc / _DAT_00592774;
    uVar4 = (int)*(short *)(local_8 + 0x265a6) & 0x8000001f;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xffffffe0) + 1;
    }
    local_b0 = -uVar4;
    uVar4 = (int)*(short *)(local_8 + 0x265a8) & 0x8000000f;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffff0) + 1;
    }
    local_b4 = 0x1e - uVar4;
    local_a0 = (int)((int)*(short *)(local_8 + 0x265a6) +
                    ((int)*(short *)(local_8 + 0x265a6) >> 0x1f & 0x1fU)) >> 5;
    local_a4 = (int)((int)*(short *)(local_8 + 0x265a8) +
                    ((int)*(short *)(local_8 + 0x265a8) >> 0x1f & 0xfU)) >> 4;
    iVar3 = (int)*(short *)(*(int *)(local_8 + 0x2659c) + 8);
    local_dc = (int)(iVar3 + (iVar3 >> 0x1f & 0x1fU)) >> 5;
    iVar3 = (int)*(short *)(*(int *)(local_8 + 0x2659c) + 10);
    local_e0 = (int)(iVar3 + (iVar3 >> 0x1f & 0xfU)) >> 4;
    local_d4 = FUN__text__0043d1a0();
    local_d8 = FUN__text__0043d200();
    for (local_18 = 0; local_18 != 0x25; local_18 = local_18 + 1) {
      for (local_14 = 0; local_14 != 0x21; local_14 = local_14 + 1) {
        local_a8 = local_14 + local_a0;
        local_ac = local_18 + local_a4;
        if ((local_a8 < *(short *)(*(int *)(local_8 + 0x2659c) + 4)) &&
           (local_ac < *(short *)(*(int *)(local_8 + 0x2659c) + 6))) {
          cVar1 = *(char *)(local_d4 +
                           local_ac * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + local_a8);
          local_cc = CONCAT31(local_cc._1_3_,cVar1);
          if ((*(char *)(local_d8 +
                        local_ac * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + local_a8) != '\0')
             && (cVar1 == '\0')) {
            local_cc = CONCAT31(local_cc._1_3_,
                                *(byte *)(local_d8 +
                                         local_ac * *(short *)(*(int *)(local_8 + 0x2659c) + 4) +
                                         local_a8) / 3);
          }
          if ((local_cc & 0xff) != 0) {
            local_d0 = (local_cc & 0xff) << 0x10 | 0xff000000 | (local_cc & 0xff) << 8 |
                       local_cc & 0xff;
            local_e4 = local_a8 / local_dc;
            local_e8 = local_ac / local_e0;
            local_ec = local_e4 + *(short *)(*(int *)(local_8 + 0x2659c) + 0xc) * local_e8;
            local_f0 = FUN__text__0041f5a0(*(undefined4 *)(local_8 + 0x263b4),local_ec);
            FUN__text__0040e210(*(undefined4 *)(local_f0 + 0x2c));
            local_e4 = local_a8 % local_dc;
            local_e8 = local_ac % local_e0;
            local_100 = local_e4 << 5;
            local_104 = (int)*(short *)(local_f0 + 0x3c);
            local_b8 = (float)local_100 / (float)local_104;
            local_108 = local_e8 << 4;
            local_10c = (int)*(short *)(local_f0 + 0x3e);
            local_bc = (float)local_108 / (float)local_10c;
            local_110 = local_e4 * 0x20 + 0x20;
            local_114 = (int)*(short *)(local_f0 + 0x3c);
            local_c0 = (float)local_110 / (float)local_114;
            local_118 = local_e8 * 0x10 + 0x10;
            local_11c = (int)*(short *)(local_f0 + 0x3e);
            local_c4 = (float)local_118 / (float)local_11c;
            local_90 = local_c8;
            local_8c = 0x3f800000;
            local_88 = local_d0;
            local_84 = 0;
            local_120 = local_b0 + local_14 * 0x20;
            local_98 = (float)local_120 - _DAT_005924c4;
            local_124 = local_b4 + local_18 * 0x10;
            local_94 = (float)local_124 - _DAT_005924c4;
            local_70 = local_c8;
            local_6c = 0x3f800000;
            local_68 = local_d0;
            local_64 = 0;
            local_128 = local_b0 + 0x20 + local_14 * 0x20;
            local_78 = (float)local_128 - _DAT_005924c4;
            local_12c = local_b4 + local_18 * 0x10;
            local_74 = (float)local_12c - _DAT_005924c4;
            local_50 = local_c8;
            local_4c = 0x3f800000;
            local_48 = local_d0;
            local_44 = 0;
            local_130 = local_b0 + 0x20 + local_14 * 0x20;
            local_58 = (float)local_130 - _DAT_005924c4;
            local_134 = local_b4 + 0x10 + local_18 * 0x10;
            local_54 = (float)local_134 - _DAT_005924c4;
            local_30 = local_c8;
            local_2c = 0x3f800000;
            local_28 = local_d0;
            local_24 = 0;
            local_138 = local_b0 + local_14 * 0x20;
            local_38 = (float)local_138 - _DAT_005924c4;
            local_13c = local_b4 + 0x10 + local_18 * 0x10;
            local_34 = (float)local_13c - _DAT_005924c4;
            local_f8 = 0;
            local_f6 = 1;
            local_f4 = 2;
            local_f2 = 3;
            local_80 = local_b8;
            local_7c = local_bc;
            local_60 = local_c0;
            local_5c = local_bc;
            local_40 = local_c0;
            local_3c = local_c4;
            local_20 = local_b8;
            local_1c = local_c4;
            (**(code **)(*local_c + 0x120))(local_c,6,2,&local_98,0x20);
            local_10 = FUN__text__0056ce80();
            if ((local_10 != 0) &&
               (iVar3 = FUN__text__00424f80("ret==((HRESULT)0x00000000L)",
                                            "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                            DAT_005ffa28 + 0xb7,0), iVar3 != 0)) {
              pcVar2 = (code *)swi(3);
              (*pcVar2)();
              return;
            }
          }
        }
      }
    }
  }
  local_8 = 0x440495;
  FUN__text__0056ce80();
  return;
}

