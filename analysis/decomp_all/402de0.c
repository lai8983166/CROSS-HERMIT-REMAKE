
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00402de0(int param_1,char *param_2,uint param_3)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  int iVar4;
  undefined4 *puVar5;
  float fVar6;
  float fVar7;
  undefined4 local_1ec [16];
  int local_1ac;
  undefined4 local_1a8;
  int local_1a4;
  undefined4 local_1a0;
  int local_19c;
  undefined4 local_198;
  undefined1 local_194 [56];
  undefined1 local_15c [56];
  undefined1 local_124 [56];
  undefined1 local_ec [56];
  undefined1 local_b4 [56];
  undefined1 local_7c [56];
  float local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  int local_2c;
  undefined4 local_28;
  undefined4 *local_24;
  char local_20;
  float local_1c;
  int local_18;
  int local_14;
  float local_10;
  float local_c;
  int local_8;
  
  puVar3 = local_1ec;
  for (iVar4 = 0x7a; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x58) != 0) {
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 0x58) + 0xdc))
              (*(undefined4 *)(param_1 + 0x58),*(undefined4 *)(param_1 + 0x670));
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0xd8))
              (*(undefined4 *)(local_8 + 0x58),*(undefined4 *)(local_8 + 0x674));
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0x130))(*(undefined4 *)(local_8 + 0x58),0x112);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0x160))(*(undefined4 *)(local_8 + 0x58),0);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 0x58) + 0x14c))
              (*(undefined4 *)(local_8 + 0x58),0,*(undefined4 *)(local_8 + 0x60),0x20);
    FUN__text__0056ce80();
    if ((param_3 & 4) != 0) {
      (**(code **)(**(int **)(local_8 + 0x58) + 0xfc))(*(undefined4 *)(local_8 + 0x58),0,0x11,2);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 0x58) + 0xfc))(*(undefined4 *)(local_8 + 0x58),0,0x10,2);
      FUN__text__0056ce80();
    }
    local_c = 0.0;
    local_10 = 0.0;
    if ((param_3 & 1) != 0) {
      FUN__text__00401e90(param_2,&local_18);
      local_c = -((float)local_18 / _DAT_005924d0) / _DAT_005924c8;
      local_10 = -((float)local_14 / _DAT_005924d0) / _DAT_005924c8;
    }
    if ((param_3 & 2) != 0) {
      (**(code **)(**(int **)(local_8 + 0x58) + 200))(*(undefined4 *)(local_8 + 0x58),0x16,1);
      FUN__text__0056ce80();
    }
    local_1c = local_c;
    local_28 = 0;
    local_2c = 0;
    (**(code **)(**(int **)(local_8 + 0x60) + 0x2c))
              (*(undefined4 *)(local_8 + 0x60),0,0,&local_24,0x2000);
    FUN__text__0056ce80();
    while( true ) {
      local_20 = *param_2;
      param_2 = param_2 + 1;
      if (local_20 == '\0') break;
      if (local_20 == '\n') {
        local_c = local_1c;
        local_19c = *(int *)(local_8 + 0x68);
        local_198 = 0;
        local_10 = local_10 -
                   ((*(float *)(local_8 + 0x7c) - *(float *)(local_8 + 0x74)) * (float)local_19c) /
                   _DAT_005924d0;
      }
      if ('\x1f' < local_20) {
        fVar6 = *(float *)(local_8 + 0x70 + (local_20 + -0x20) * 0x10);
        local_34 = *(float *)(local_8 + 0x74 + (local_20 + -0x20) * 0x10);
        local_38 = *(float *)(local_8 + 0x78 + (local_20 + -0x20) * 0x10);
        fVar7 = *(float *)(local_8 + 0x7c + (local_20 + -0x20) * 0x10);
        local_1a4 = *(int *)(local_8 + 100);
        local_1a0 = 0;
        local_40 = ((local_38 - fVar6) * (float)local_1a4) /
                   (_DAT_005924d0 * *(float *)(local_8 + 0x6c));
        local_1ac = *(int *)(local_8 + 0x68);
        local_1a8 = 0;
        local_44 = ((fVar7 - local_34) * (float)local_1ac) /
                   (_DAT_005924d0 * *(float *)(local_8 + 0x6c));
        local_3c = fVar7;
        local_30 = fVar6;
        if (local_20 != ' ') {
          uVar1 = FUN__text__00403580(0,0,0xbf800000);
          uVar2 = FUN__text__00403580(local_c + _DAT_005924c0,local_10 + _DAT_005924c0,0);
          puVar3 = (undefined4 *)FUN__text__00403480(local_7c,uVar2,uVar1,fVar6,fVar7);
          puVar5 = local_24;
          for (iVar4 = 8; iVar4 != 0; iVar4 = iVar4 + -1) {
            *puVar5 = *puVar3;
            puVar3 = puVar3 + 1;
            puVar5 = puVar5 + 1;
          }
          local_24 = local_24 + 8;
          fVar6 = local_30;
          fVar7 = local_34;
          uVar1 = FUN__text__00403580(0,0,0xbf800000);
          uVar2 = FUN__text__00403580(local_c + _DAT_005924c0,local_10 + local_44,0);
          puVar3 = (undefined4 *)FUN__text__00403480(local_b4,uVar2,uVar1,fVar6,fVar7);
          puVar5 = local_24;
          for (iVar4 = 8; iVar4 != 0; iVar4 = iVar4 + -1) {
            *puVar5 = *puVar3;
            puVar3 = puVar3 + 1;
            puVar5 = puVar5 + 1;
          }
          local_24 = local_24 + 8;
          fVar6 = local_38;
          fVar7 = local_3c;
          uVar1 = FUN__text__00403580(0,0,0xbf800000);
          uVar2 = FUN__text__00403580(local_c + local_40,local_10 + _DAT_005924c0,0);
          puVar3 = (undefined4 *)FUN__text__00403480(local_ec,uVar2,uVar1,fVar6,fVar7);
          puVar5 = local_24;
          for (iVar4 = 8; iVar4 != 0; iVar4 = iVar4 + -1) {
            *puVar5 = *puVar3;
            puVar3 = puVar3 + 1;
            puVar5 = puVar5 + 1;
          }
          local_24 = local_24 + 8;
          fVar6 = local_38;
          fVar7 = local_34;
          uVar1 = FUN__text__00403580(0,0,0xbf800000);
          uVar2 = FUN__text__00403580(local_c + local_40,local_10 + local_44,0);
          puVar3 = (undefined4 *)FUN__text__00403480(local_124,uVar2,uVar1,fVar6,fVar7);
          puVar5 = local_24;
          for (iVar4 = 8; iVar4 != 0; iVar4 = iVar4 + -1) {
            *puVar5 = *puVar3;
            puVar3 = puVar3 + 1;
            puVar5 = puVar5 + 1;
          }
          local_24 = local_24 + 8;
          fVar6 = local_38;
          fVar7 = local_3c;
          uVar1 = FUN__text__00403580(0,0,0xbf800000);
          uVar2 = FUN__text__00403580(local_c + local_40,local_10 + _DAT_005924c0,0);
          puVar3 = (undefined4 *)FUN__text__00403480(local_15c,uVar2,uVar1,fVar6,fVar7);
          puVar5 = local_24;
          for (iVar4 = 8; iVar4 != 0; iVar4 = iVar4 + -1) {
            *puVar5 = *puVar3;
            puVar3 = puVar3 + 1;
            puVar5 = puVar5 + 1;
          }
          local_24 = local_24 + 8;
          fVar6 = local_30;
          fVar7 = local_34;
          uVar1 = FUN__text__00403580(0,0,0xbf800000);
          uVar2 = FUN__text__00403580(local_c + _DAT_005924c0,local_10 + local_44,0);
          puVar3 = (undefined4 *)FUN__text__00403480(local_194,uVar2,uVar1,fVar6,fVar7);
          puVar5 = local_24;
          for (iVar4 = 8; iVar4 != 0; iVar4 = iVar4 + -1) {
            *puVar5 = *puVar3;
            puVar3 = puVar3 + 1;
            puVar5 = puVar5 + 1;
          }
          local_24 = local_24 + 8;
          local_2c = local_2c + 2;
          if (0x126 < (uint)(local_2c * 3)) {
            (**(code **)(**(int **)(local_8 + 0x60) + 0x30))(*(undefined4 *)(local_8 + 0x60));
            FUN__text__0056ce80();
            (**(code **)(**(int **)(local_8 + 0x58) + 0x118))
                      (*(undefined4 *)(local_8 + 0x58),4,0,local_2c);
            FUN__text__0056ce80();
            (**(code **)(**(int **)(local_8 + 0x60) + 0x2c))
                      (*(undefined4 *)(local_8 + 0x60),0,0,&local_24,0x2000);
            FUN__text__0056ce80();
            local_2c = 0;
          }
        }
        local_c = local_c + local_40;
      }
    }
    (**(code **)(**(int **)(local_8 + 0x60) + 0x30))(*(undefined4 *)(local_8 + 0x60));
    FUN__text__0056ce80();
    if (local_2c != 0) {
      (**(code **)(**(int **)(local_8 + 0x58) + 0x118))
                (*(undefined4 *)(local_8 + 0x58),4,0,local_2c);
      FUN__text__0056ce80();
    }
    (**(code **)(**(int **)(local_8 + 0x58) + 0xd8))
              (*(undefined4 *)(local_8 + 0x58),*(undefined4 *)(local_8 + 0x670));
    FUN__text__0056ce80();
  }
  local_8 = 0x40347a;
  FUN__text__0056ce80();
  return;
}

