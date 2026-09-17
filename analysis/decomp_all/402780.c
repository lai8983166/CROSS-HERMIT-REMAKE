
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN__text__00402780(int param_1,float param_2,float param_3,undefined4 param_4,char *param_5,
                   uint param_6)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  float fVar6;
  float fVar7;
  undefined4 local_190 [16];
  int local_150;
  undefined4 local_14c;
  int local_148;
  undefined4 local_144;
  int local_140;
  undefined4 local_13c;
  undefined1 local_138 [44];
  undefined1 local_10c [44];
  undefined1 local_e0 [44];
  undefined1 local_b4 [44];
  undefined1 local_88 [44];
  undefined1 local_5c [44];
  float local_30;
  float local_2c;
  float local_28;
  float local_24;
  float local_20;
  float local_1c;
  char local_18;
  int local_14;
  undefined4 *local_10;
  float local_c;
  int local_8;
  
  puVar2 = local_190;
  for (iVar3 = 99; iVar3 != 0; iVar3 = iVar3 + -1) {
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
    if ((param_6 & 4) != 0) {
      (**(code **)(**(int **)(local_8 + 0x58) + 0xfc))(*(undefined4 *)(local_8 + 0x58),0,0x11,2);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 0x58) + 0xfc))(*(undefined4 *)(local_8 + 0x58),0,0x10,2);
      FUN__text__0056ce80();
    }
    local_c = param_2;
    local_10 = (undefined4 *)0x0;
    local_14 = 0;
    (**(code **)(**(int **)(local_8 + 0x60) + 0x2c))
              (*(undefined4 *)(local_8 + 0x60),0,0,&local_10,0x2000);
    FUN__text__0056ce80();
    while (*param_5 != '\0') {
      local_18 = *param_5;
      param_5 = param_5 + 1;
      if (local_18 == '\n') {
        param_2 = local_c;
        local_140 = *(int *)(local_8 + 0x68);
        local_13c = 0;
        param_3 = (*(float *)(local_8 + 0x7c) - *(float *)(local_8 + 0x74)) * (float)local_140 +
                  param_3;
      }
      if ('\x1f' < local_18) {
        fVar6 = *(float *)(local_8 + 0x70 + (local_18 + -0x20) * 0x10);
        local_20 = *(float *)(local_8 + 0x74 + (local_18 + -0x20) * 0x10);
        local_24 = *(float *)(local_8 + 0x78 + (local_18 + -0x20) * 0x10);
        fVar7 = *(float *)(local_8 + 0x7c + (local_18 + -0x20) * 0x10);
        local_148 = *(int *)(local_8 + 100);
        local_144 = 0;
        local_2c = ((local_24 - fVar6) * (float)local_148) / *(float *)(local_8 + 0x6c);
        local_150 = *(int *)(local_8 + 0x68);
        local_14c = 0;
        local_30 = ((fVar7 - local_20) * (float)local_150) / *(float *)(local_8 + 0x6c);
        local_28 = fVar7;
        local_1c = fVar6;
        if (local_18 != ' ') {
          uVar5 = param_4;
          uVar1 = FUN__text__004035d0((param_2 + _DAT_005924c0) - _DAT_005924c4,
                                      (param_3 + local_30) - _DAT_005924c4,0x3f666666,0x3f800000);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_5c,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_10;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_10 = local_10 + 7;
          uVar5 = param_4;
          fVar6 = local_1c;
          fVar7 = local_20;
          uVar1 = FUN__text__004035d0((param_2 + _DAT_005924c0) - _DAT_005924c4,
                                      (param_3 + _DAT_005924c0) - _DAT_005924c4,0x3f666666,
                                      0x3f800000);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_88,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_10;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_10 = local_10 + 7;
          uVar5 = param_4;
          fVar6 = local_24;
          fVar7 = local_28;
          uVar1 = FUN__text__004035d0((param_2 + local_2c) - _DAT_005924c4,
                                      (param_3 + local_30) - _DAT_005924c4,0x3f666666,0x3f800000);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_b4,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_10;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_10 = local_10 + 7;
          uVar5 = param_4;
          fVar6 = local_24;
          fVar7 = local_20;
          uVar1 = FUN__text__004035d0((param_2 + local_2c) - _DAT_005924c4,
                                      (param_3 + _DAT_005924c0) - _DAT_005924c4,0x3f666666,
                                      0x3f800000);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_e0,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_10;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_10 = local_10 + 7;
          uVar5 = param_4;
          fVar6 = local_24;
          fVar7 = local_28;
          uVar1 = FUN__text__004035d0((param_2 + local_2c) - _DAT_005924c4,
                                      (param_3 + local_30) - _DAT_005924c4,0x3f666666,0x3f800000);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_10c,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_10;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_10 = local_10 + 7;
          uVar5 = param_4;
          fVar6 = local_1c;
          fVar7 = local_20;
          uVar1 = FUN__text__004035d0((param_2 + _DAT_005924c0) - _DAT_005924c4,
                                      (param_3 + _DAT_005924c0) - _DAT_005924c4,0x3f666666,
                                      0x3f800000);
          puVar2 = (undefined4 *)FUN__text__004026d0(local_138,uVar1,uVar5,fVar6,fVar7);
          puVar4 = local_10;
          for (iVar3 = 7; iVar3 != 0; iVar3 = iVar3 + -1) {
            *puVar4 = *puVar2;
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          }
          local_10 = local_10 + 7;
          local_14 = local_14 + 2;
          if (0x126 < (uint)(local_14 * 3)) {
            (**(code **)(**(int **)(local_8 + 0x60) + 0x30))(*(undefined4 *)(local_8 + 0x60));
            FUN__text__0056ce80();
            (**(code **)(**(int **)(local_8 + 0x58) + 0x118))
                      (*(undefined4 *)(local_8 + 0x58),4,0,local_14);
            FUN__text__0056ce80();
            local_10 = (undefined4 *)0x0;
            (**(code **)(**(int **)(local_8 + 0x60) + 0x2c))
                      (*(undefined4 *)(local_8 + 0x60),0,0,&local_10,0x2000);
            FUN__text__0056ce80();
            local_14 = 0;
          }
        }
        param_2 = param_2 + local_2c;
      }
    }
    (**(code **)(**(int **)(local_8 + 0x60) + 0x30))(*(undefined4 *)(local_8 + 0x60));
    FUN__text__0056ce80();
    if (local_14 != 0) {
      (**(code **)(**(int **)(local_8 + 0x58) + 0x118))
                (*(undefined4 *)(local_8 + 0x58),4,0,local_14);
      FUN__text__0056ce80();
    }
    (**(code **)(**(int **)(local_8 + 0x58) + 0xd8))
              (*(undefined4 *)(local_8 + 0x58),*(undefined4 *)(local_8 + 0x670));
    FUN__text__0056ce80();
  }
  local_8 = 0x402da3;
  FUN__text__0056ce80();
  return;
}

