
void FUN__text__0055cbb3(uint *param_1,int *param_2,byte *param_3)

{
  uint *puVar1;
  byte bVar2;
  byte *pbVar3;
  int iVar4;
  uint *puVar5;
  byte *pbVar6;
  undefined4 uVar7;
  uint uVar8;
  byte *pbVar9;
  undefined4 local_38;
  undefined4 local_34;
  byte *local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  byte *local_1c;
  byte *local_18;
  byte *local_14;
  byte *local_10;
  byte *local_c;
  uint local_8;
  
  puVar5 = param_1;
  local_c = (byte *)param_2[1];
  local_8 = param_1[8];
  local_10 = (byte *)param_1[0xd];
  if (local_10 < (byte *)param_1[0xc]) {
    local_14 = (byte *)param_1[0xc] + (-1 - (int)local_10);
  }
  else {
    local_14 = (byte *)(param_1[0xb] - (int)local_10);
  }
  uVar8 = *param_1;
  param_1 = (uint *)param_1[7];
  pbVar9 = (byte *)*param_2;
  while (local_18 = pbVar9, uVar8 < 10) {
    switch((&switchD_.text::0055cc2f::switchdataD__text__0055d326)[uVar8]) {
    case (undefined *)0x55cc5a:
      for (; pbVar9 = local_18, param_1 < (byte *)0x3; param_1 = (uint *)((int)param_1 + 8)) {
        if (local_c == (byte *)0x0) goto LAB__text__0055d253;
        param_3 = (byte *)0x0;
        local_c = local_c + -1;
        local_8 = local_8 | (uint)*local_18 << ((byte)param_1 & 0x1f);
        local_18 = local_18 + 1;
      }
      uVar8 = (local_8 & 7) >> 1;
      puVar5[6] = local_8 & 1;
      if (uVar8 == 0) {
        uVar8 = (uint)((int)param_1 + -3) & 7;
        local_8 = (local_8 >> 3) >> (sbyte)uVar8;
        param_1 = (uint *)((byte *)((int)param_1 + -3) + -uVar8);
        *puVar5 = 1;
      }
      else if (uVar8 == 1) {
        FUN__text__00560528(&local_2c,&local_28,&local_24,&local_20,param_2);
        uVar8 = FUN__text__0055fa78(local_2c,local_28,local_24,local_20,param_2);
        puVar5[1] = uVar8;
        if (uVar8 == 0) goto LAB__text__0055d2c7;
        local_8 = local_8 >> 3;
        param_1 = (uint *)((int)param_1 + -3);
        *puVar5 = 6;
      }
      else {
        if (uVar8 == 2) {
          local_8 = local_8 >> 3;
          uVar8 = 3;
          param_1 = (uint *)((int)param_1 + -3);
          goto LAB__text__0055ccb5;
        }
        if (uVar8 == 3) {
          *puVar5 = 9;
          param_2[6] = (int)"invalid block type";
          puVar5[8] = local_8 >> 3;
          param_1 = (uint *)((int)param_1 + -3);
          param_3 = (byte *)0xfffffffd;
          goto LAB__text__0055cc05;
        }
      }
      break;
    case (undefined *)0x55cd24:
      for (; pbVar9 = local_18, param_1 < (byte *)0x20; param_1 = (uint *)((int)param_1 + 8)) {
        if (local_c == (byte *)0x0) goto LAB__text__0055d253;
        param_3 = (byte *)0x0;
        local_c = local_c + -1;
        local_8 = local_8 | (uint)*local_18 << ((byte)param_1 & 0x1f);
        local_18 = local_18 + 1;
      }
      if (~local_8 >> 0x10 != (local_8 & 0xffff)) {
        *puVar5 = 9;
        param_2[6] = (int)"invalid stored block lengths";
        goto switchD__text__0055cc2f_caseD_55d20b;
      }
      puVar5[1] = local_8 & 0xffff;
      param_1 = (uint *)0x0;
      local_8 = 0;
      if (puVar5[1] == 0) goto LAB__text__0055ce66;
      uVar8 = 2;
LAB__text__0055ccb5:
      *puVar5 = uVar8;
      break;
    case (undefined *)0x55cd85:
      if (local_c == (byte *)0x0) {
LAB__text__0055d253:
        puVar5[8] = local_8;
        puVar5[7] = (uint)param_1;
        param_2[1] = 0;
        goto LAB__text__0055cc0e;
      }
      if (local_14 == (byte *)0x0) {
        local_14 = (byte *)0x0;
        if (local_10 == (byte *)puVar5[0xb]) {
          pbVar6 = (byte *)puVar5[0xc];
          pbVar3 = (byte *)puVar5[10];
          if (pbVar3 != pbVar6) {
            if (pbVar3 < pbVar6) {
              local_14 = pbVar6 + (-1 - (int)pbVar3);
            }
            else {
              local_14 = (byte *)puVar5[0xb] + -(int)pbVar3;
            }
            local_10 = pbVar3;
            if (local_14 != (byte *)0x0) goto LAB__text__0055ce26;
          }
        }
        puVar5[0xd] = (uint)local_10;
        param_3 = (byte *)FUN__text__00560557(puVar5,param_2,param_3);
        local_1c = (byte *)puVar5[0xc];
        local_10 = (byte *)puVar5[0xd];
        if (local_10 < local_1c) {
          local_14 = local_1c + (-1 - (int)local_10);
        }
        else {
          local_14 = (byte *)(puVar5[0xb] - (int)local_10);
        }
        local_30 = (byte *)puVar5[0xb];
        if (local_10 == local_30) {
          pbVar6 = (byte *)puVar5[10];
          if (pbVar6 != local_1c) {
            local_10 = pbVar6;
            if (pbVar6 < local_1c) {
              local_14 = local_1c + (-1 - (int)pbVar6);
            }
            else {
              local_14 = local_30 + -(int)pbVar6;
            }
          }
        }
        if (local_14 == (byte *)0x0) {
          puVar5[8] = local_8;
          puVar5[7] = (uint)param_1;
          param_2[1] = (int)local_c;
          param_2[2] = (int)(pbVar9 + (param_2[2] - *param_2));
          goto LAB__text__0055cc18;
        }
      }
LAB__text__0055ce26:
      param_3 = (byte *)0x0;
      pbVar9 = (byte *)puVar5[1];
      if (local_c < (byte *)puVar5[1]) {
        pbVar9 = local_c;
      }
      if (local_14 < pbVar9) {
        pbVar9 = local_14;
      }
      pbVar6 = local_18 + (int)pbVar9;
      local_c = local_c + -(int)pbVar9;
      pbVar3 = local_10 + (int)pbVar9;
      local_14 = local_14 + -(int)pbVar9;
      for (uVar8 = (uint)pbVar9 >> 2; uVar8 != 0; uVar8 = uVar8 - 1) {
        *(undefined4 *)local_10 = *(undefined4 *)local_18;
        local_18 = local_18 + 4;
        local_10 = local_10 + 4;
      }
      for (uVar8 = (uint)pbVar9 & 3; uVar8 != 0; uVar8 = uVar8 - 1) {
        *local_10 = *local_18;
        local_18 = local_18 + 1;
        local_10 = local_10 + 1;
      }
      puVar1 = puVar5 + 1;
      *puVar1 = *puVar1 - (int)pbVar9;
      local_18 = pbVar6;
      local_10 = pbVar3;
      if (*puVar1 == 0) {
LAB__text__0055ce66:
        uVar8 = -(uint)(puVar5[6] != 0) & 7;
        goto LAB__text__0055ccb5;
      }
      break;
    case (undefined *)0x55ce75:
      for (; param_1 < (byte *)0xe; param_1 = (uint *)((int)param_1 + 8)) {
        if (local_c == (byte *)0x0) goto LAB__text__0055d253;
        param_3 = (byte *)0x0;
        local_c = local_c + -1;
        local_8 = local_8 | (uint)*pbVar9 << ((byte)param_1 & 0x1f);
        pbVar9 = pbVar9 + 1;
      }
      puVar5[1] = local_8 & 0x3fff;
      if ((0x1d < (local_8 & 0x1f)) || (uVar8 = (local_8 & 0x3fff) >> 5 & 0x1f, 0x1d < uVar8)) {
        *puVar5 = 9;
        param_2[6] = (int)"too many length or distance symbols";
        goto switchD__text__0055cc2f_caseD_55d20b;
      }
      uVar8 = (*(code *)param_2[8])(param_2[10],uVar8 + 0x102 + (local_8 & 0x1f),4);
      puVar5[3] = uVar8;
      if (uVar8 != 0) {
        local_8 = local_8 >> 0xe;
        param_1 = (uint *)((int)param_1 + -0xe);
        puVar5[2] = 0;
        *puVar5 = 4;
        goto switchD__text__0055cc2f_caseD_55cf44;
      }
LAB__text__0055d2c7:
      param_3 = (byte *)0xfffffffc;
      goto LAB__text__0055cbfc;
    case (undefined *)0x55cf44:
switchD__text__0055cc2f_caseD_55cf44:
      while (puVar5[2] < (puVar5[1] >> 10) + 4) {
        for (; param_1 < (byte *)0x3; param_1 = (uint *)((int)param_1 + 8)) {
          if (local_c == (byte *)0x0) goto LAB__text__0055d253;
          param_3 = (byte *)0x0;
          local_c = local_c + -1;
          local_8 = local_8 | (uint)*pbVar9 << ((byte)param_1 & 0x1f);
          pbVar9 = pbVar9 + 1;
        }
        *(uint *)(puVar5[3] + *(int *)(&DAT_005d42c8 + puVar5[2] * 4) * 4) = local_8 & 7;
        puVar5[2] = puVar5[2] + 1;
        param_1 = (uint *)((int)param_1 + -3);
        local_8 = local_8 >> 3;
      }
      while (puVar5[2] < 0x13) {
        *(undefined4 *)(puVar5[3] + *(int *)(&DAT_005d42c8 + puVar5[2] * 4) * 4) = 0;
        puVar5[2] = puVar5[2] + 1;
      }
      puVar5[4] = 7;
      local_14 = (byte *)FUN__text__005603a6(puVar5[3],puVar5 + 4,puVar5 + 5,puVar5[9],param_2);
      if (local_14 == (byte *)0x0) {
        puVar5[2] = 0;
        *puVar5 = 5;
        goto switchD__text__0055cc2f_caseD_55d0c2;
      }
      (*(code *)param_2[9])(param_2[10],puVar5[3]);
      goto LAB__text__0055d2b7;
    case (undefined *)0x55d0c2:
switchD__text__0055cc2f_caseD_55d0c2:
      while (puVar5[2] < (puVar5[1] >> 5 & 0x1f) + 0x102 + (puVar5[1] & 0x1f)) {
        for (; param_1 < (byte *)puVar5[4]; param_1 = (uint *)((int)param_1 + 8)) {
          if (local_c == (byte *)0x0) goto LAB__text__0055d253;
          param_3 = (byte *)0x0;
          local_c = local_c + -1;
          local_8 = local_8 | (uint)*pbVar9 << ((byte)param_1 & 0x1f);
          pbVar9 = pbVar9 + 1;
        }
        iVar4 = puVar5[5] + (*(uint *)(&DAT_00761920 + (int)puVar5[4] * 4) & local_8) * 8;
        bVar2 = *(byte *)(iVar4 + 1);
        local_14 = (byte *)(uint)bVar2;
        local_30 = *(byte **)(iVar4 + 4);
        if (local_30 < (byte *)0x10) {
          local_8 = local_8 >> (bVar2 & 0x1f);
          param_1 = (uint *)((int)param_1 + -(int)local_14);
          *(byte **)(puVar5[3] + puVar5[2] * 4) = local_30;
          puVar5[2] = puVar5[2] + 1;
        }
        else {
          if (local_30 == (byte *)0x12) {
            pbVar6 = (byte *)0x7;
          }
          else {
            pbVar6 = local_30 + -0xe;
          }
          local_18 = (byte *)((uint)(local_30 == (byte *)0x12) * 8 + 3);
          for (; param_1 < pbVar6 + (int)local_14; param_1 = (uint *)((int)param_1 + 8)) {
            if (local_c == (byte *)0x0) goto LAB__text__0055d253;
            param_3 = (byte *)0x0;
            local_c = local_c + -1;
            local_8 = local_8 | (uint)*pbVar9 << ((byte)param_1 & 0x1f);
            pbVar9 = pbVar9 + 1;
          }
          local_8 = local_8 >> (bVar2 & 0x1f);
          local_18 = local_18 + (*(uint *)(&DAT_00761920 + (int)pbVar6 * 4) & local_8);
          local_8 = local_8 >> ((byte)pbVar6 & 0x1f);
          param_1 = (uint *)((int)param_1 + -(int)(pbVar6 + (int)local_14));
          uVar8 = puVar5[2];
          if ((byte *)((puVar5[1] >> 5 & 0x1f) + 0x102 + (puVar5[1] & 0x1f)) < local_18 + uVar8) {
LAB__text__0055d26b:
            (*(code *)param_2[9])(param_2[10],puVar5[3]);
            *puVar5 = 9;
            param_2[6] = (int)"invalid bit length repeat";
            puVar5[8] = local_8;
            puVar5[7] = (uint)param_1;
            param_2[1] = (int)local_c;
            param_2[2] = (int)(pbVar9 + (param_2[2] - *param_2));
            *param_2 = (int)pbVar9;
            puVar5[0xd] = (uint)local_10;
            FUN__text__00560557(puVar5,param_2,0xfffffffd);
            return;
          }
          if (local_30 == (byte *)0x10) {
            if (uVar8 == 0) goto LAB__text__0055d26b;
            uVar7 = *(undefined4 *)((puVar5[3] - 4) + uVar8 * 4);
          }
          else {
            uVar7 = 0;
          }
          do {
            *(undefined4 *)(puVar5[3] + uVar8 * 4) = uVar7;
            uVar8 = uVar8 + 1;
            local_18 = local_18 + -1;
          } while (local_18 != (byte *)0x0);
          puVar5[2] = uVar8;
          local_18 = (byte *)0x0;
        }
      }
      puVar5[5] = 0;
      local_1c = (byte *)0x9;
      local_18 = (byte *)0x6;
      local_14 = (byte *)FUN__text__00560425((puVar5[1] & 0x1f) + 0x101,(puVar5[1] >> 5 & 0x1f) + 1,
                                             puVar5[3],&local_1c,&local_18,&local_38,&local_34,
                                             puVar5[9],param_2);
      (*(code *)param_2[9])(param_2[10],puVar5[3]);
      if (local_14 == (byte *)0x0) {
        uVar8 = FUN__text__0055fa78(local_1c,local_18,local_38,local_34,param_2);
        if (uVar8 == 0) goto LAB__text__0055d2c7;
        puVar5[1] = uVar8;
        *puVar5 = 6;
        goto switchD__text__0055cc2f_caseD_55d163;
      }
LAB__text__0055d2b7:
      param_3 = local_14;
      if (local_14 == (byte *)0xfffffffd) {
        *puVar5 = 9;
      }
      goto LAB__text__0055cbfc;
    case (undefined *)0x55d163:
switchD__text__0055cc2f_caseD_55d163:
      puVar5[8] = local_8;
      puVar5[7] = (uint)param_1;
      param_2[1] = (int)local_c;
      param_2[2] = (int)(pbVar9 + (param_2[2] - *param_2));
      *param_2 = (int)pbVar9;
      puVar5[0xd] = (uint)local_10;
      param_3 = (byte *)FUN__text__0055faac(puVar5,param_2,param_3);
      if (param_3 != (byte *)0x1) goto LAB__text__0055cc1d;
      param_3 = (byte *)0x0;
      FUN__text__00560010(puVar5[1],param_2);
      local_c = (byte *)param_2[1];
      local_18 = (byte *)*param_2;
      local_8 = puVar5[8];
      param_1 = (uint *)puVar5[7];
      local_10 = (byte *)puVar5[0xd];
      if (local_10 < (byte *)puVar5[0xc]) {
        local_14 = (byte *)puVar5[0xc] + (-1 - (int)local_10);
      }
      else {
        local_14 = (byte *)(puVar5[0xb] - (int)local_10);
      }
      if (puVar5[6] != 0) {
        *puVar5 = 7;
        goto switchD__text__0055cc2f_caseD_55d2d4;
      }
      *puVar5 = 0;
      break;
    case (undefined *)0x55d20b:
switchD__text__0055cc2f_caseD_55d20b:
      param_3 = (byte *)0xfffffffd;
      goto LAB__text__0055cbfc;
    case (undefined *)0x55d2d4:
switchD__text__0055cc2f_caseD_55d2d4:
      pbVar9 = local_18;
      puVar5[0xd] = (uint)local_10;
      param_3 = (byte *)FUN__text__00560557(puVar5,param_2,param_3);
      local_10 = (byte *)puVar5[0xd];
      if ((byte *)puVar5[0xc] == local_10) {
        *puVar5 = 8;
        goto switchD__text__0055cc2f_caseD_55d31f;
      }
      puVar5[8] = local_8;
      puVar5[7] = (uint)param_1;
      param_2[1] = (int)local_c;
      iVar4 = *param_2;
      *param_2 = (int)pbVar9;
      param_2[2] = (int)(pbVar9 + (param_2[2] - iVar4));
      puVar5[0xd] = (uint)local_10;
      goto LAB__text__0055cc1d;
    case (undefined *)0x55d31f:
switchD__text__0055cc2f_caseD_55d31f:
      param_3 = (byte *)0x1;
      goto LAB__text__0055cbfc;
    }
    pbVar9 = local_18;
    uVar8 = *puVar5;
  }
  param_3 = (byte *)0xfffffffe;
LAB__text__0055cbfc:
  puVar5[8] = local_8;
LAB__text__0055cc05:
  puVar5[7] = (uint)param_1;
  param_2[1] = (int)local_c;
LAB__text__0055cc0e:
  param_2[2] = (int)(pbVar9 + (param_2[2] - *param_2));
LAB__text__0055cc18:
  *param_2 = (int)pbVar9;
  puVar5[0xd] = (uint)local_10;
LAB__text__0055cc1d:
  FUN__text__00560557(puVar5,param_2,param_3);
  return;
}

