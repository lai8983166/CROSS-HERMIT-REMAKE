
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN__text__00401fd0(int param_1,float param_2,float param_3,undefined4 param_4,float param_5,
                   float param_6,undefined4 param_7,char *param_8,uint param_9)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  float fVar6;
  float fVar7;
  undefined4 local_1e4 [16];
  uint local_1a4;
  undefined4 uStack_1a0;
  uint local_19c;
  undefined4 uStack_198;
  int local_194;
  undefined4 local_190;
  int local_18c;
  undefined4 local_188;
  uint local_184;
  undefined4 uStack_180;
  int local_17c;
  undefined4 local_178;
  uint local_174;
  undefined4 local_170;
  uint local_16c;
  undefined4 local_168;
  undefined1 local_164 [44];
  undefined1 local_138 [44];
  undefined1 local_10c [44];
  undefined1 local_e0 [44];
  undefined1 local_b4 [44];
  undefined1 local_88 [44];
  float local_5c;
  float local_58;
  float local_54;
  float local_50;
  float local_4c;
  float local_48;
  char local_44;
  int local_40;
  undefined4 *local_3c;
  float local_38;
  float local_34;
  undefined4 local_30;
  undefined4 local_2c;
  float local_28;
  float local_24;
  undefined1 local_20 [8];
  uint local_18;
  uint local_14;
  int local_8;
  
  puVar2 = local_1e4;
  for (iVar3 = 0x78; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0x58) != 0) {
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 0x58) + 0xdc))
              (*(undefined4 *)(param_1 + 0x58),*(undefined4 *)(param_1 + 0x670));
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0xd8))
              (*(undefined4 *)(local_8 + 0x58),*(undefined4 *)(local_8 + 0x674));
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0x130))(*(undefined4 *)(local_8 + 0x58),0x144);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0x160))(*(undefined4 *)(local_8 + 0x58),0);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0x14c))
              (*(undefined4 *)(local_8 + 0x58),0,*(undefined4 *)(local_8 + 0x60),0x1c);
    FUN__text__0056ce80();
    if ((param_9 & 4) != 0) {
      (**(code **)(**(int **)(local_8 + 0x58) + 0xfc))(*(undefined4 *)(local_8 + 0x58),0,0x11,2);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 0x58) + 0xfc))(*(undefined4 *)(local_8 + 0x58),0,0x10,2);
      FUN__text__0056ce80();
    }
    (**(code **)(**(int **)(local_8 + 0x58) + 0xa4))(*(undefined4 *)(local_8 + 0x58),local_20);
    FUN__text__0056ce80();
    local_16c = local_18;
    local_168 = 0;
    local_34 = ((param_2 + _DAT_005924cc) * (float)(int)local_18) / _DAT_005924c8;
    local_174 = local_14;
    local_170 = 0;
    local_28 = ((param_3 + _DAT_005924cc) * (float)(int)local_14) / _DAT_005924c8;
    local_2c = param_4;
    local_30 = 0x3f800000;
    local_17c = *(int *)(local_8 + 0x68);
    local_178 = 0;
    local_38 = (*(float *)(local_8 + 0x7c) - *(float *)(local_8 + 0x74)) * (float)local_17c;
    local_40 = 0;
    local_24 = local_34;
    (**(code **)(**(int **)(local_8 + 0x60) + 0x2c))
              (*(undefined4 *)(local_8 + 0x60),0,0,&local_3c,0x2000);
    FUN__text__0056ce80();
    while (*param_8 != '\0') {
      local_44 = *param_8;
      param_8 = param_8 + 1;
      if (local_44 == '\n') {
        local_24 = local_34;
        local_184 = local_14;
        uStack_180 = 0;
        local_28 = (float)local_14 * param_6 + local_28;
      }
      if ('\x1f' < local_44) {
        fVar6 = *(float *)(local_8 + 0x70 + (local_44 + -0x20) * 0x10);
        local_4c = *(float *)(local_8 + 0x74 + (local_44 + -0x20) * 0x10);
        local_50 = *(float *)(local_8 + 0x78 + (local_44 + -0x20) * 0x10);
        fVar7 = *(float *)(local_8 + 0x7c + (local_44 + -0x20) * 0x10);
        local_18c = *(int *)(local_8 + 100);
        local_188 = 0;
        local_194 = *(int *)(local_8 + 0x68);
        local_190 = 0;
        local_19c = local_18;
        uStack_198 = 0;
        local_58 = (((float)local_18 * param_5) / local_38) * (local_50 - fVar6) * (float)local_18c;
        local_1a4 = local_14;
        uStack_1a0 = 0;
        local_5c = (((float)local_14 * param_6) / local_38) * (fVar7 - local_4c) * (float)local_194;
        local_54 = fVar7;
        local_48 = fVar6;
        if (local_44 != ' ') {
          uVar5 = param_7;
          uVar1 = FUN__text__004035d0((local_24 + _DAT_005924c0) - _DAT_005924c4,
                                      (local_28 + local_5c) - _DAT_005924c4,local_2c,local_30);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_88,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_3c;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_3c = local_3c + 7;
          uVar5 = param_7;
          fVar6 = local_48;
          fVar7 = local_4c;
          uVar1 = FUN__text__004035d0((local_24 + _DAT_005924c0) - _DAT_005924c4,
                                      (local_28 + _DAT_005924c0) - _DAT_005924c4,local_2c,local_30);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_b4,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_3c;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_3c = local_3c + 7;
          uVar5 = param_7;
          fVar6 = local_50;
          fVar7 = local_54;
          uVar1 = FUN__text__004035d0((local_24 + local_58) - _DAT_005924c4,
                                      (local_28 + local_5c) - _DAT_005924c4,local_2c,local_30);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_e0,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_3c;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_3c = local_3c + 7;
          uVar5 = param_7;
          fVar6 = local_50;
          fVar7 = local_4c;
          uVar1 = FUN__text__004035d0((local_24 + local_58) - _DAT_005924c4,
                                      (local_28 + _DAT_005924c0) - _DAT_005924c4,local_2c,local_30);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_10c,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_3c;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_3c = local_3c + 7;
          uVar5 = param_7;
          fVar6 = local_50;
          fVar7 = local_54;
          uVar1 = FUN__text__004035d0((local_24 + local_58) - _DAT_005924c4,
                                      (local_28 + local_5c) - _DAT_005924c4,local_2c,local_30);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_138,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_3c;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_3c = local_3c + 7;
          uVar5 = param_7;
          fVar6 = local_48;
          fVar7 = local_4c;
          uVar1 = FUN__text__004035d0((local_24 + _DAT_005924c0) - _DAT_005924c4,
                                      (local_28 + _DAT_005924c0) - _DAT_005924c4,local_2c,local_30);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_164,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_3c;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_3c = local_3c + 7;
          local_40 = local_40 + 2;
          if (0x126 < (uint)(local_40 * 3)) {
            (**(code **)(**(int **)(local_8 + 0x60) + 0x30))(*(undefined4 *)(local_8 + 0x60));
            FUN__text__0056ce80();
            (**(code **)(**(int **)(local_8 + 0x58) + 0x118))
                      (*(undefined4 *)(local_8 + 0x58),4,0,local_40);
            FUN__text__0056ce80();
            (**(code **)(**(int **)(local_8 + 0x60) + 0x2c))
                      (*(undefined4 *)(local_8 + 0x60),0,0,&local_3c,0x2000);
            FUN__text__0056ce80();
            local_40 = 0;
          }
        }
        local_24 = local_24 + local_58;
      }
    }
    (**(code **)(**(int **)(local_8 + 0x60) + 0x30))(*(undefined4 *)(local_8 + 0x60));
    FUN__text__0056ce80();
    if (local_40 != 0) {
      (**(code **)(**(int **)(local_8 + 0x58) + 0x118))
                (*(undefined4 *)(local_8 + 0x58),4,0,local_40);
      FUN__text__0056ce80();
    }
    (**(code **)(**(int **)(local_8 + 0x58) + 0xd8))
              (*(undefined4 *)(local_8 + 0x58),*(undefined4 *)(local_8 + 0x670));
    FUN__text__0056ce80();
  }
  local_8 = 0x4026c2;
  FUN__text__0056ce80();
  return;
}

