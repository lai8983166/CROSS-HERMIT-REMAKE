
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0043e540(int param_1,int param_2)

{
  char cVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_148 [16];
  int local_108;
  int local_104;
  int local_100;
  int local_fc;
  int local_f8;
  int local_f4;
  int local_f0;
  int local_ec;
  int local_e8;
  int local_e4;
  int local_e0;
  int local_dc;
  int local_d8;
  int local_d4;
  int local_d0;
  int local_cc;
  uint local_c8;
  uint local_c4;
  float local_c0;
  float local_bc;
  float local_b8;
  float local_b4;
  float local_b0;
  int local_ac;
  int local_a8;
  int local_a4;
  int local_a0;
  int local_9c;
  int local_98;
  float local_94;
  float local_90;
  float local_8c;
  undefined4 local_88;
  uint local_84;
  undefined4 local_80;
  float local_7c;
  float local_78;
  float local_74;
  float local_70;
  float local_6c;
  undefined4 local_68;
  uint local_64;
  undefined4 local_60;
  float local_5c;
  float local_58;
  float local_54;
  float local_50;
  float local_4c;
  undefined4 local_48;
  uint local_44;
  undefined4 local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  float local_2c;
  undefined4 local_28;
  uint local_24;
  undefined4 local_20;
  float local_1c;
  float local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar4 = local_148;
  for (iVar3 = 0x51; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (((*(int *)(param_1 + 0x2659c) != 0) && (DAT_007a49fc != 0)) &&
     (local_8 = param_1, local_c = (int *)FUN__text__004142b0(),
     *(short *)(DAT_007a49fc + 0xb288) == 0)) {
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
    (**(code **)(*local_c + 0xf4))(local_c,0,*(undefined4 *)(local_8 + 0xdc));
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0x130))(local_c,0x1c4);
    FUN__text__0056ce80();
    local_c0 = (float)param_2 / _DAT_00592774;
    uVar2 = (int)*(short *)(local_8 + 0x265a6) & 0x8000001f;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xffffffe0) + 1;
    }
    local_a8 = -uVar2;
    uVar2 = (int)*(short *)(local_8 + 0x265a8) & 0x8000000f;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffff0) + 1;
    }
    local_ac = 0x1e - uVar2;
    local_98 = (int)((int)*(short *)(local_8 + 0x265a6) +
                    ((int)*(short *)(local_8 + 0x265a6) >> 0x1f & 0x1fU)) >> 5;
    local_9c = (int)((int)*(short *)(local_8 + 0x265a8) +
                    ((int)*(short *)(local_8 + 0x265a8) >> 0x1f & 0xfU)) >> 4;
    for (local_14 = 0; local_14 != 0x25; local_14 = local_14 + 1) {
      for (local_10 = 0; local_10 != 0x21; local_10 = local_10 + 1) {
        local_a0 = local_10 + local_98;
        local_a4 = local_14 + local_9c;
        cVar1 = *(char *)(*(int *)(local_8 + 0x2659c) + 0x15 +
                         (local_a4 * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + local_a0) * 6);
        local_c4 = CONCAT31(local_c4._1_3_,cVar1);
        if (((*(byte *)(**(int **)(local_8 + 0x265a0) +
                       (local_a4 * *(short *)(*(int *)(local_8 + 0x2659c) + 4) + local_a0) * 2) &
             0x80) != 0) && (cVar1 == '\0')) {
          local_c4 = CONCAT31(local_c4._1_3_,0x60);
        }
        local_c8 = (local_c4 & 0xff) << 0x10 | 0xff000000 | (local_c4 & 0xff) << 8 | local_c4 & 0xff
        ;
        local_cc = local_a0 * 0x20;
        local_d0 = (int)*(short *)(local_8 + 0xec);
        local_b0 = (float)local_cc / (float)local_d0;
        local_d4 = local_a4 * 0x10;
        local_d8 = (int)*(short *)(local_8 + 0xee);
        local_b4 = (float)local_d4 / (float)local_d8;
        local_dc = local_a0 * 0x20 + 0x20;
        local_e0 = (int)*(short *)(local_8 + 0xec);
        local_b8 = (float)local_dc / (float)local_e0;
        local_e4 = local_a4 * 0x10 + 0x10;
        local_e8 = (int)*(short *)(local_8 + 0xee);
        local_bc = (float)local_e4 / (float)local_e8;
        local_8c = local_c0;
        local_88 = 0x3f800000;
        local_80 = 0;
        local_ec = local_a8 + local_10 * 0x20;
        local_94 = (float)local_ec;
        local_f0 = local_ac + local_14 * 0x10;
        local_90 = (float)local_f0;
        local_6c = local_c0;
        local_68 = 0x3f800000;
        local_60 = 0;
        local_f4 = local_a8 + 0x20 + local_10 * 0x20;
        local_74 = (float)local_f4;
        local_f8 = local_ac + local_14 * 0x10;
        local_70 = (float)local_f8;
        local_4c = local_c0;
        local_48 = 0x3f800000;
        local_40 = 0;
        local_fc = local_a8 + 0x20 + local_10 * 0x20;
        local_54 = (float)local_fc;
        local_100 = local_ac + 0x10 + local_14 * 0x10;
        local_50 = (float)local_100;
        local_2c = local_c0;
        local_28 = 0x3f800000;
        local_20 = 0;
        local_104 = local_a8 + local_10 * 0x20;
        local_34 = (float)local_104;
        local_108 = local_ac + 0x10 + local_14 * 0x10;
        local_30 = (float)local_108;
        local_84 = local_c8;
        local_7c = local_b0;
        local_78 = local_b4;
        local_64 = local_c8;
        local_5c = local_b8;
        local_58 = local_b4;
        local_44 = local_c8;
        local_3c = local_b8;
        local_38 = local_bc;
        local_24 = local_c8;
        local_1c = local_b0;
        local_18 = local_bc;
        (**(code **)(*local_c + 0x120))(local_c,6,2,&local_94,0x20);
        FUN__text__0056ce80();
      }
    }
  }
  local_8 = 0x43eb8d;
  FUN__text__0056ce80();
  return;
}

