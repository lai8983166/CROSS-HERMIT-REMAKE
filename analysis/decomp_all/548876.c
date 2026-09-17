
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint * __thiscall
FUN__text__00548876(int param_1,uint *param_2,uint *param_3,uint param_4,int *param_5,uint param_6,
                   undefined4 param_7,uint *param_8)

{
  int *piVar1;
  code *pcVar2;
  int iVar3;
  uint uVar4;
  uint *puVar5;
  int *piVar6;
  uint uVar7;
  uint *puVar8;
  undefined4 *puVar9;
  undefined4 uVar10;
  uint uStack_148;
  undefined4 uStack_144;
  undefined1 *puStack_140;
  uint uStack_13c;
  int *piStack_138;
  uint uStack_134;
  undefined4 uStack_130;
  undefined4 *puStack_12c;
  undefined4 local_11c [4];
  int local_10c;
  uint local_88;
  uint local_84;
  uint local_80;
  uint local_7c;
  float local_78;
  float local_74;
  uint local_70 [10];
  undefined4 local_48;
  undefined4 local_44;
  int local_40;
  uint local_3c;
  int local_38;
  uint *local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  uint local_18;
  uint local_14;
  uint *local_10;
  uint *local_c;
  uint local_8;
  
  piVar6 = param_5;
  if ((param_3 == (uint *)0x0) || (param_5 == (int *)0x0)) {
LAB__text__00548a99:
    param_2 = (uint *)0x0;
  }
  else {
    piVar1 = param_5 + 2;
    iVar3 = *param_5;
    local_14 = param_5[3] - param_5[1];
    param_5 = (int *)(*piVar1 - iVar3);
    local_8 = local_14;
    if (param_8 != (uint *)0x0) {
      puStack_12c = local_11c;
      local_11c[0] = 0x94;
      uStack_130 = 0x5488c9;
      (*API_KERNEL32_DLL_GetVersionExA)();
      pcVar2 = API_KERNEL32_DLL_WideCharToMultiByte;
      if (local_10c != 2) {
        puStack_12c = (undefined4 *)0x0;
        uStack_130 = 0;
        uStack_134 = 0;
        piStack_138 = (int *)0x0;
        uStack_13c = param_4;
        puStack_140 = (undefined1 *)param_3;
        uStack_144 = 0;
        uStack_148 = 0;
        local_c = (uint *)(*API_KERNEL32_DLL_WideCharToMultiByte)();
        FUN__text__0056e230();
        param_8 = &uStack_148;
        (*pcVar2)(0,0,param_3,param_4,&uStack_148,local_c,0,0);
        param_3 = param_8;
        param_8 = (uint *)0x0;
        param_4 = (uint)local_c;
        local_14 = local_8;
      }
    }
    puStack_12c = param_2;
    uStack_130 = *(undefined4 *)(param_1 + 0x6c);
    local_20 = 0;
    local_1c = 0;
    local_18 = (uint)param_5;
    uStack_134 = 0x54893d;
    iVar3 = (*API_GDI32_DLL_SelectObject)();
    if (*(int *)(param_1 + 0xa8) == 0) {
      *(int *)(param_1 + 0xa8) = iVar3;
    }
    uStack_134 = param_6 | 0x400;
    piStack_138 = &local_20;
    uStack_13c = param_4;
    puStack_140 = (undefined1 *)param_3;
    uStack_144 = *(undefined4 *)(param_1 + 0x6c);
    if (param_8 == (uint *)0x0) {
      uStack_148 = 0x548976;
      param_2 = (uint *)(*API_USER32_DLL_DrawTextA)();
    }
    else {
      uStack_148 = 0x54896e;
      param_2 = (uint *)(*API_USER32_DLL_DrawTextW)();
    }
    local_18 = local_18 - local_20;
    local_20 = 0;
    local_14 = local_14 - local_1c;
    local_1c = 0;
    uVar4 = local_8;
    if ((param_6 & 0x400) == 0) {
      if (((param_6 & 0x100) == 0) && (param_5 <= local_18)) {
        local_18 = (uint)param_5;
      }
      param_5 = (int *)local_18;
      local_18 = (uint)param_5;
      uVar4 = local_14;
      if (((param_6 & 0x100) == 0) && (uVar4 = local_14, local_8 <= local_14)) {
        local_14 = local_8;
        uVar4 = local_8;
      }
    }
    local_8 = uVar4;
    if ((param_6 & 2) == 0) {
      local_30 = *piVar6;
      if ((param_6 & 1) != 0) {
        local_30 = (int)((local_30 - local_18) + piVar6[2]) >> 1;
      }
      local_28 = local_30 + local_18;
    }
    else {
      local_28 = piVar6[2];
      local_30 = local_28 - local_18;
    }
    if ((param_6 & 8) == 0) {
      local_2c = piVar6[1];
      if ((param_6 & 4) != 0) {
        local_2c = (int)((local_2c - local_14) + piVar6[3]) >> 1;
      }
      local_24 = local_2c + local_14;
    }
    else {
      local_24 = piVar6[3];
      local_2c = local_24 - local_14;
    }
    if ((param_6 & 0x400) != 0) {
      *piVar6 = local_30;
      piVar6[1] = local_2c;
      piVar6[2] = local_28;
      piVar6[3] = local_24;
      return param_2;
    }
    if ((*(uint *)(param_1 + 0x74) < param_5) || (*(uint *)(param_1 + 0x78) < local_8)) {
      local_10 = (uint *)0x0;
      puVar5 = (uint *)(param_1 + 0x70);
      puVar8 = local_70;
      for (iVar3 = 10; iVar3 != 0; iVar3 = iVar3 + -1) {
        *puVar8 = *puVar5;
        puVar5 = puVar5 + 1;
        puVar8 = puVar8 + 1;
      }
      for (; local_70[1] < param_5; local_70[1] = local_70[1] + ((int)local_70[1] >> 1)) {
      }
      for (; local_70[2] < local_8; local_70[2] = local_70[2] + ((int)local_70[2] >> 1)) {
      }
      local_70[2] = -local_70[2];
      uStack_148 = 0;
      iVar3 = (*API_GDI32_DLL_CreateDIBSection)
                        (*(undefined4 *)(param_1 + 0x6c),local_70,0,&param_2,0);
      if (iVar3 == 0) goto LAB__text__00548a99;
      local_70[2] = -local_70[2];
      (*API_GDI32_DLL_SelectObject)(*(undefined4 *)(param_1 + 0x6c),iVar3);
      (*API_GDI32_DLL_DeleteObject)(*(int *)(param_1 + 0x98));
      *(uint **)(param_1 + 0xa0) = param_2;
      *(uint *)(param_1 + 0x74) = local_70[1];
      *(int *)(param_1 + 0x98) = iVar3;
      *(uint *)(param_1 + 0x78) = local_70[2];
    }
    uVar4 = (uint)(*(ushort *)(param_1 + 0x7e) >> 3);
    param_2 = *(uint **)(param_1 + 0xa0);
    local_10 = (uint *)(uVar4 * (int)param_5);
    uVar4 = *(int *)(param_1 + 0x74) * uVar4 + 3 & 0xfffffffc;
    local_c = (uint *)(uVar4 * local_8 + (int)param_2);
    for (; param_2 < local_c; param_2 = (uint *)((int)param_2 + uVar4)) {
      puVar5 = param_2;
      for (uVar7 = (uint)local_10 >> 2; uVar7 != 0; uVar7 = uVar7 - 1) {
        *puVar5 = 0;
        puVar5 = puVar5 + 1;
      }
      for (uVar7 = (uint)local_10 & 3; uVar7 != 0; uVar7 = uVar7 - 1) {
        *(undefined1 *)puVar5 = 0;
        puVar5 = (uint *)((int)puVar5 + 1);
      }
    }
    uStack_148 = param_6;
    if (param_8 == (uint *)0x0) {
      param_2 = (uint *)(*API_USER32_DLL_DrawTextA)
                                  (*(undefined4 *)(param_1 + 0x6c),param_3,param_4,&local_20);
    }
    else {
      param_2 = (uint *)(*API_USER32_DLL_DrawTextW)();
    }
    if (*(int *)(param_1 + 0x54) != 0x15) {
      for (puVar5 = *(uint **)(param_1 + 0xa0); puVar5 < local_c;
          puVar5 = (uint *)((int)puVar5 + (uVar4 - (int)local_10))) {
        puVar8 = (uint *)((int)puVar5 + (int)local_10);
        for (; puVar5 < puVar8; puVar5 = puVar5 + 1) {
          *puVar5 = *puVar5 << 0x18 | 0xffffff;
        }
      }
    }
    local_c = *(uint **)(param_1 + 0x60);
    if (local_c == (uint *)0x0) {
      FUN__text__00548514();
    }
    param_8 = (uint *)0x0;
    if (local_8 != 0) {
      do {
        param_4 = *(int *)(param_1 + 0x5c) + (int)param_8;
        if (local_8 < param_4) {
          param_4 = local_8;
        }
        uVar7 = 0;
        uVar4 = (uint)param_8;
        if (param_5 != (int *)0x0) {
          param_6 = param_4 - (int)param_8;
          do {
            local_80 = *(int *)(param_1 + 0x58) + uVar7;
            if (param_5 < local_80) {
              local_80 = (uint)param_5;
            }
            local_40 = local_80 - uVar7;
            local_48 = 0;
            local_44 = 0;
            local_3c = param_6;
            local_88 = uVar7;
            local_84 = uVar4;
            local_7c = param_4;
            if (*(int *)(param_1 + 0x54) == 0x15) {
              piVar6 = *(int **)(param_1 + 0x30 + *(int *)(param_1 + 8) * 4);
              if (*(int *)(param_1 + 0x50) == 0) {
                uVar10 = 0x800;
                puVar9 = &local_48;
              }
              else {
                uVar10 = 0x2800;
                puVar9 = (undefined4 *)0x0;
              }
              iVar3 = (**(code **)(*piVar6 + 0x24))(piVar6,&local_38,puVar9,uVar10);
              if (iVar3 < 0) goto LAB__text__00548d69;
              piVar6 = (int *)(*(int *)(param_1 + 0xa0) +
                              (*(int *)(param_1 + 0x74) * uVar4 + uVar7) * 4);
              for (param_3 = local_34; param_3 < (uint *)(local_38 * local_3c + (int)local_34);
                  param_3 = (uint *)((int)param_3 + local_38 + local_40 * -4)) {
                local_10 = param_3 + local_40;
                for (; param_3 < local_10; param_3 = param_3 + 1) {
                  *param_3 = *piVar6 << 0x18 | 0xffffff;
                  piVar6 = piVar6 + 1;
                }
                piVar6 = piVar6 + (*(int *)(param_1 + 0x74) - local_40);
                uVar4 = (uint)param_8;
              }
              piVar6 = *(int **)(param_1 + 0x30 + *(int *)(param_1 + 8) * 4);
              (**(code **)(*piVar6 + 0x28))(piVar6);
            }
            else {
              iVar3 = FUN__text__00526e9f(*(undefined4 *)
                                           (param_1 + 0x30 + *(int *)(param_1 + 8) * 4),0,&local_48,
                                          *(undefined4 *)(param_1 + 0xa0),
                                          *(undefined4 *)(param_1 + 0xa4),
                                          (uint)(*(ushort *)(param_1 + 0x7e) >> 3) *
                                          *(int *)(param_1 + 0x74),0,&local_88,2,0);
              if (iVar3 < 0) goto LAB__text__00548d69;
            }
            local_78 = (float)(int)(local_30 + uVar7);
            if ((int)(local_30 + uVar7) < 0) {
              local_78 = local_78 + _DAT_005d0a44;
            }
            param_3 = (uint *)(local_2c + uVar4);
            local_74 = (float)(int)param_3;
            if ((int)param_3 < 0) {
              local_74 = local_74 + _DAT_005d0a44;
            }
            iVar3 = (**(code **)(**(int **)(param_1 + 0xc) + 0x14))
                              (*(int **)(param_1 + 0xc),
                               *(undefined4 *)(param_1 + 0x10 + *(int *)(param_1 + 8) * 4),&local_48
                               ,0,0,0,&local_78,param_7);
            if (iVar3 < 0) goto LAB__text__00548d69;
            if (*(int *)(param_1 + 0x50) == 0) {
              *(uint *)(param_1 + 8) = *(int *)(param_1 + 8) + 1U & 7;
            }
            uVar7 = uVar7 + *(int *)(param_1 + 0x58);
          } while (uVar7 < param_5);
        }
        param_8 = (uint *)(uVar4 + *(int *)(param_1 + 0x5c));
      } while (param_8 < local_8);
    }
LAB__text__00548d69:
    if (local_c == (uint *)0x0) {
      FUN__text__005485a1();
    }
  }
  return param_2;
}

