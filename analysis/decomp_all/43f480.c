
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0043f480(int param_1,int param_2)

{
  char cVar1;
  code *pcVar2;
  uint uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_170 [16];
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
  int local_fc;
  int local_f8;
  int local_f4;
  undefined2 local_f0;
  undefined2 local_ee;
  undefined2 local_ec;
  undefined2 local_ea;
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
  int local_9c;
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
  
  puVar5 = local_170;
  for (iVar4 = 0x5b; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_9c = 0;
  if ((*(int *)(param_1 + 0x2659c) != 0) && (DAT_007a49fc != 0)) {
    local_8 = param_1;
    local_c = (int *)FUN__text__004142b0();
    (**(code **)(*local_c + 0xfc))(local_c,0,4,4);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,5,2);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,6,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,1,4);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,2,2);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,3,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,0x12,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,0x10,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,0x11,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x1b,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x1b,1);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0xf,1);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x18,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x19,5);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0xe,1);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x13,2);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x14,1);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0x130))(local_c,0x1c4);
    FUN__text__0056ce80();
    local_c8 = (float)param_2 / _DAT_00592774;
    uVar3 = (int)*(short *)(local_8 + 0x265a6) & 0x8000001f;
    if ((int)uVar3 < 0) {
      uVar3 = (uVar3 - 1 | 0xffffffe0) + 1;
    }
    local_b0 = -uVar3;
    uVar3 = (int)*(short *)(local_8 + 0x265a8) & 0x8000000f;
    if ((int)uVar3 < 0) {
      uVar3 = (uVar3 - 1 | 0xfffffff0) + 1;
    }
    local_b4 = 0x1e - uVar3;
    local_a0 = (int)((int)*(short *)(local_8 + 0x265a6) +
                    ((int)*(short *)(local_8 + 0x265a6) >> 0x1f & 0x1fU)) >> 5;
    local_a4 = (int)((int)*(short *)(local_8 + 0x265a8) +
                    ((int)*(short *)(local_8 + 0x265a8) >> 0x1f & 0xfU)) >> 4;
    iVar4 = (int)*(short *)(*(int *)(local_8 + 0x2659c) + 8);
    local_d4 = (int)(iVar4 + (iVar4 >> 0x1f & 0x1fU)) >> 5;
    iVar4 = (int)*(short *)(*(int *)(local_8 + 0x2659c) + 10);
    local_d8 = (int)(iVar4 + (iVar4 >> 0x1f & 0xfU)) >> 4;
    for (local_18 = 0; local_18 != 0x13; local_18 = local_18 + 1) {
      for (local_14 = 0; local_14 != 0x21; local_14 = local_14 + 1) {
        local_a8 = local_14 + local_a0;
        local_ac = local_18 + local_a4;
        if ((local_a8 < *(short *)(*(int *)(local_8 + 0x2659c) + 4)) &&
           (local_ac < *(short *)(*(int *)(local_8 + 0x2659c) + 6))) {
          cVar1 = *(char *)(*(int *)(local_8 + 0x2659c) + 0x15 +
                           (local_ac * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + local_a8) * 6);
          local_cc = CONCAT31(local_cc._1_3_,cVar1);
          if (((*(byte *)(**(int **)(local_8 + 0x265a0) +
                         (local_ac * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + local_a8) * 2) &
               0x80) != 0) && (cVar1 == '\0')) {
            local_cc = CONCAT31(local_cc._1_3_,0x60);
          }
          if ((local_cc & 0xff) != 0) {
            local_d0 = (local_cc & 0xff) << 0x10 | 0xff000000 | (local_cc & 0xff) << 8 |
                       local_cc & 0xff;
            local_dc = local_a8 / local_d4;
            local_e0 = local_ac / local_d8;
            local_e4 = local_dc + *(short *)(*(int *)(local_8 + 0x2659c) + 0xc) * local_e0;
            local_e8 = FUN__text__0041f5a0(*(undefined4 *)(local_8 + 0x263b4),local_e4);
            if (local_9c != *(int *)(local_e8 + 0x2c)) {
              (**(code **)(*local_c + 0xf4))(local_c,0,*(undefined4 *)(local_e8 + 0x2c));
              FUN__text__0056ce80();
              local_9c = *(int *)(local_e8 + 0x2c);
            }
            local_dc = local_a8 % local_d4;
            local_e0 = local_ac % local_d8;
            local_f4 = local_dc << 5;
            local_f8 = (int)*(short *)(local_e8 + 0x3c);
            local_b8 = (float)local_f4 / (float)local_f8;
            local_fc = local_e0 << 4;
            local_100 = (int)*(short *)(local_e8 + 0x3e);
            local_bc = (float)local_fc / (float)local_100;
            local_104 = local_dc * 0x20 + 0x20;
            local_108 = (int)*(short *)(local_e8 + 0x3c);
            local_c0 = (float)local_104 / (float)local_108;
            local_10c = local_e0 * 0x10 + 0x10;
            local_110 = (int)*(short *)(local_e8 + 0x3e);
            local_c4 = (float)local_10c / (float)local_110;
            local_90 = local_c8;
            local_8c = 0x3f800000;
            local_88 = local_d0;
            local_84 = 0;
            local_114 = local_b0 + local_14 * 0x20;
            local_98 = (float)local_114;
            local_118 = local_b4 + local_18 * 0x10;
            local_94 = (float)local_118;
            local_70 = local_c8;
            local_6c = 0x3f800000;
            local_68 = local_d0;
            local_64 = 0;
            local_11c = local_b0 + 0x20 + local_14 * 0x20;
            local_78 = (float)local_11c;
            local_120 = local_b4 + local_18 * 0x10;
            local_74 = (float)local_120;
            local_50 = local_c8;
            local_4c = 0x3f800000;
            local_48 = local_d0;
            local_44 = 0;
            local_124 = local_b0 + 0x20 + local_14 * 0x20;
            local_58 = (float)local_124;
            local_128 = local_b4 + 0x10 + local_18 * 0x10;
            local_54 = (float)local_128;
            local_30 = local_c8;
            local_2c = 0x3f800000;
            local_28 = local_d0;
            local_24 = 0;
            local_12c = local_b0 + local_14 * 0x20;
            local_38 = (float)local_12c;
            local_130 = local_b4 + 0x10 + local_18 * 0x10;
            local_34 = (float)local_130;
            local_f0 = 0;
            local_ee = 1;
            local_ec = 2;
            local_ea = 3;
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
               (iVar4 = FUN__text__00424f80("ret==((HRESULT)0x00000000L)",
                                            "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                            DAT_005ffa24 + 0xa7,0), iVar4 != 0)) {
              pcVar2 = (code *)swi(3);
              (*pcVar2)();
              return;
            }
          }
        }
      }
    }
  }
  local_8 = 0x43fd0b;
  FUN__text__0056ce80();
  return;
}

