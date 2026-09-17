
void FUN__text1__00844daf(uint *param_1,int *param_2,undefined4 param_3)

{
  byte bVar1;
  uint uVar2;
  int iVar3;
  undefined4 uVar4;
  uint local_80;
  uint local_7c;
  uint local_78;
  int local_74;
  uint local_70;
  uint local_6c;
  uint local_68;
  uint local_64;
  uint local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  uint local_48;
  undefined4 local_44;
  int local_40;
  uint local_3c;
  int local_38;
  uint local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  uint local_c;
  byte *local_8;
  
  local_8 = (byte *)*param_2;
  local_20 = param_2[1];
  local_10 = param_1[8];
  local_18 = param_1[7];
  local_c = param_1[0xd];
  if (local_c < param_1[0xc]) {
    local_58 = (param_1[0xc] - local_c) - 1;
  }
  else {
    local_58 = param_1[0xb] - local_c;
  }
  local_1c = local_58;
  do {
    switch(*param_1) {
    case 0:
      for (; local_18 < 3; local_18 = local_18 + 8) {
        if (local_20 == 0) {
          param_1[8] = local_10;
          param_1[7] = local_18;
          param_2[1] = 0;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          param_1[0xd] = local_c;
          FUN__text1__00847af0(param_1,param_2,param_3);
          return;
        }
        param_3 = 0;
        local_20 = local_20 - 1;
        local_10 = local_10 | (uint)*local_8 << ((byte)local_18 & 0x1f);
        local_8 = local_8 + 1;
      }
      local_14 = local_10 & 7;
      param_1[6] = local_10 & 1;
      switch(local_14 >> 1) {
      case 0:
        local_14 = local_18 - 3 & 7;
        local_10 = (local_10 >> 3) >> (sbyte)local_14;
        local_18 = (local_18 - 3) - local_14;
        *param_1 = 1;
        break;
      case 1:
        FUN__text1__00847abb(&local_2c,&local_24,&local_28,&local_30,param_2);
        uVar2 = FUN__text1__008461f0(local_2c,local_24,local_28,local_30,param_2);
        param_1[1] = uVar2;
        if (param_1[1] == 0) {
          param_1[8] = local_10;
          param_1[7] = local_18;
          param_2[1] = local_20;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          param_1[0xd] = local_c;
          FUN__text1__00847af0(param_1,param_2,0xfffffffc);
          return;
        }
        local_10 = local_10 >> 3;
        local_18 = local_18 - 3;
        *param_1 = 6;
        break;
      case 2:
        local_10 = local_10 >> 3;
        local_18 = local_18 - 3;
        *param_1 = 3;
        break;
      case 3:
        local_10 = local_10 >> 3;
        local_18 = local_18 - 3;
        *param_1 = 9;
        param_2[6] = (int)"invalid block type";
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = local_20;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,0xfffffffd);
        return;
      }
      break;
    case 1:
      for (; local_18 < 0x20; local_18 = local_18 + 8) {
        if (local_20 == 0) {
          param_1[8] = local_10;
          param_1[7] = local_18;
          param_2[1] = 0;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          param_1[0xd] = local_c;
          FUN__text1__00847af0(param_1,param_2,param_3);
          return;
        }
        param_3 = 0;
        local_20 = local_20 - 1;
        local_10 = local_10 | (uint)*local_8 << ((byte)local_18 & 0x1f);
        local_8 = local_8 + 1;
      }
      if (~local_10 >> 0x10 != (local_10 & 0xffff)) {
        *param_1 = 9;
        param_2[6] = (int)"invalid stored block lengths";
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = local_20;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,0xfffffffd);
        return;
      }
      param_1[1] = local_10 & 0xffff;
      local_18 = 0;
      local_10 = 0;
      if (param_1[1] == 0) {
        local_64 = -(uint)(param_1[6] != 0) & 7;
      }
      else {
        local_64 = 2;
      }
      *param_1 = local_64;
      break;
    case 2:
      if (local_20 == 0) {
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = 0;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,param_3);
        return;
      }
      if (local_1c == 0) {
        if ((local_c == param_1[0xb]) && (param_1[0xc] != param_1[10])) {
          local_c = param_1[10];
          if (local_c < param_1[0xc]) {
            local_68 = (param_1[0xc] - local_c) - 1;
          }
          else {
            local_68 = param_1[0xb] - local_c;
          }
          local_1c = local_68;
        }
        if (local_1c == 0) {
          param_1[0xd] = local_c;
          uVar4 = FUN__text1__00847af0(param_1,param_2,param_3);
          local_c = param_1[0xd];
          if (local_c < param_1[0xc]) {
            local_6c = (param_1[0xc] - local_c) - 1;
          }
          else {
            local_6c = param_1[0xb] - local_c;
          }
          local_1c = local_6c;
          if ((local_c == param_1[0xb]) && (param_1[0xc] != param_1[10])) {
            local_c = param_1[10];
            if (local_c < param_1[0xc]) {
              local_70 = (param_1[0xc] - local_c) - 1;
            }
            else {
              local_70 = param_1[0xb] - local_c;
            }
            local_1c = local_70;
          }
          if (local_1c == 0) {
            param_1[8] = local_10;
            param_1[7] = local_18;
            param_2[1] = local_20;
            param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
            *param_2 = (int)local_8;
            param_1[0xd] = local_c;
            FUN__text1__00847af0(param_1,param_2,uVar4);
            return;
          }
        }
      }
      param_3 = 0;
      local_14 = param_1[1];
      if (local_20 < local_14) {
        local_14 = local_20;
      }
      if (local_1c < local_14) {
        local_14 = local_1c;
      }
      FUN__text1__00848490(local_c,local_8,local_14);
      local_8 = local_8 + local_14;
      local_20 = local_20 - local_14;
      local_c = local_c + local_14;
      local_1c = local_1c - local_14;
      param_1[1] = param_1[1] - local_14;
      if (param_1[1] == 0) {
        *param_1 = -(uint)(param_1[6] != 0) & 7;
      }
      break;
    case 3:
      for (; local_18 < 0xe; local_18 = local_18 + 8) {
        if (local_20 == 0) {
          param_1[8] = local_10;
          param_1[7] = local_18;
          param_2[1] = 0;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          param_1[0xd] = local_c;
          FUN__text1__00847af0(param_1,param_2,param_3);
          return;
        }
        param_3 = 0;
        local_20 = local_20 - 1;
        local_10 = local_10 | (uint)*local_8 << ((byte)local_18 & 0x1f);
        local_8 = local_8 + 1;
      }
      local_14 = local_10 & 0x3fff;
      param_1[1] = local_14;
      if ((0x1d < (local_10 & 0x1f)) || (0x1d < (local_14 >> 5 & 0x1f))) {
        *param_1 = 9;
        param_2[6] = (int)"too many length or distance symbols";
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = local_20;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,0xfffffffd);
        return;
      }
      local_14 = (local_10 & 0x1f) + 0x102 + (local_14 >> 5 & 0x1f);
      uVar2 = (*(code *)param_2[8])(param_2[10],local_14,4);
      param_1[3] = uVar2;
      if (param_1[3] == 0) {
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = local_20;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,0xfffffffc);
        return;
      }
      local_10 = local_10 >> 0xe;
      local_18 = local_18 - 0xe;
      param_1[2] = 0;
      *param_1 = 4;
    case 4:
      while (param_1[2] < (param_1[1] >> 10) + 4) {
        for (; local_18 < 3; local_18 = local_18 + 8) {
          if (local_20 == 0) {
            param_1[8] = local_10;
            param_1[7] = local_18;
            param_2[1] = 0;
            param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
            *param_2 = (int)local_8;
            param_1[0xd] = local_c;
            FUN__text1__00847af0(param_1,param_2,param_3);
            return;
          }
          param_3 = 0;
          local_20 = local_20 - 1;
          local_10 = local_10 | (uint)*local_8 << ((byte)local_18 & 0x1f);
          local_8 = local_8 + 1;
        }
        *(uint *)(param_1[3] + *(int *)(&DAT_00873d24 + param_1[2] * 4) * 4) = local_10 & 7;
        param_1[2] = param_1[2] + 1;
        local_10 = local_10 >> 3;
        local_18 = local_18 - 3;
      }
      while (param_1[2] < 0x13) {
        *(undefined4 *)(param_1[3] + *(int *)(&DAT_00873d24 + param_1[2] * 4) * 4) = 0;
        param_1[2] = param_1[2] + 1;
      }
      param_1[4] = 7;
      iVar3 = FUN__text1__00846fc0(param_1[3],param_1 + 4,param_1 + 5,param_1[9],param_2);
      if (iVar3 != 0) {
        local_14 = iVar3;
        if (iVar3 == -3) {
          (*(code *)param_2[9])(param_2[10],param_1[3]);
          *param_1 = 9;
        }
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = local_20;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,iVar3);
        return;
      }
      param_1[2] = 0;
      *param_1 = 5;
    case 5:
      while (param_1[2] < (param_1[1] & 0x1f) + 0x102 + (param_1[1] >> 5 & 0x1f)) {
        local_14 = param_1[4];
        for (; local_18 < local_14; local_18 = local_18 + 8) {
          if (local_20 == 0) {
            param_1[8] = local_10;
            param_1[7] = local_18;
            param_2[1] = 0;
            param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
            *param_2 = (int)local_8;
            param_1[0xd] = local_c;
            FUN__text1__00847af0(param_1,param_2,param_3);
            return;
          }
          param_3 = 0;
          local_20 = local_20 - 1;
          local_10 = local_10 | (uint)*local_8 << ((byte)local_18 & 0x1f);
          local_8 = local_8 + 1;
        }
        local_38 = param_1[5] + (local_10 & *(uint *)(&DAT_008701c8 + local_14 * 4)) * 8;
        bVar1 = *(byte *)(local_38 + 1);
        local_14 = (uint)bVar1;
        local_34 = *(uint *)(local_38 + 4);
        if (local_34 < 0x10) {
          local_10 = local_10 >> (bVar1 & 0x1f);
          local_18 = local_18 - local_14;
          *(uint *)(param_1[3] + param_1[2] * 4) = local_34;
          param_1[2] = param_1[2] + 1;
        }
        else {
          if (local_34 == 0x12) {
            local_74 = 7;
          }
          else {
            local_74 = local_34 - 0xe;
          }
          local_3c = local_74;
          local_40 = (-(uint)(local_34 != 0x12) & 0xfffffff8) + 0xb;
          for (; local_18 < local_14 + local_74; local_18 = local_18 + 8) {
            if (local_20 == 0) {
              param_1[8] = local_10;
              param_1[7] = local_18;
              param_2[1] = 0;
              param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
              *param_2 = (int)local_8;
              param_1[0xd] = local_c;
              FUN__text1__00847af0(param_1,param_2,param_3);
              return;
            }
            param_3 = 0;
            local_20 = local_20 - 1;
            local_10 = local_10 | (uint)*local_8 << ((byte)local_18 & 0x1f);
            local_8 = local_8 + 1;
          }
          local_10 = local_10 >> (bVar1 & 0x1f);
          local_40 = local_40 + (local_10 & *(uint *)(&DAT_008701c8 + local_74 * 4));
          local_10 = local_10 >> ((byte)local_74 & 0x1f);
          local_18 = (local_18 - local_14) - local_74;
          local_3c = param_1[2];
          local_14 = param_1[1];
          if (((local_14 & 0x1f) + 0x102 + (local_14 >> 5 & 0x1f) < local_3c + local_40) ||
             ((local_34 == 0x10 && (local_3c == 0)))) {
            (*(code *)param_2[9])(param_2[10],param_1[3]);
            *param_1 = 9;
            param_2[6] = (int)"invalid bit length repeat";
            param_1[8] = local_10;
            param_1[7] = local_18;
            param_2[1] = local_20;
            param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
            *param_2 = (int)local_8;
            param_1[0xd] = local_c;
            FUN__text1__00847af0(param_1,param_2,0xfffffffd);
            return;
          }
          if (local_34 == 0x10) {
            local_78 = *(uint *)((param_1[3] - 4) + local_3c * 4);
          }
          else {
            local_78 = 0;
          }
          local_34 = local_78;
          do {
            *(uint *)(param_1[3] + local_3c * 4) = local_78;
            local_3c = local_3c + 1;
            local_40 = local_40 + -1;
          } while (local_40 != 0);
          param_1[2] = local_3c;
          local_40 = 0;
        }
      }
      param_1[5] = 0;
      local_50 = 9;
      local_44 = 6;
      local_14 = param_1[1];
      local_14 = FUN__text1__00847936
                           ((local_14 & 0x1f) + 0x101,(local_14 >> 5 & 0x1f) + 1,param_1[3],
                            &local_50,&local_44,&local_4c,&local_54,param_1[9],param_2);
      if (local_14 != 0) {
        if (local_14 == 0xfffffffd) {
          (*(code *)param_2[9])(param_2[10],param_1[3]);
          *param_1 = 9;
        }
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = local_20;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,local_14);
        return;
      }
      local_48 = FUN__text1__008461f0(local_50,local_44,local_4c,local_54,param_2);
      if (local_48 == 0) {
        param_1[8] = local_10;
        param_1[7] = local_18;
        param_2[1] = local_20;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        param_1[0xd] = local_c;
        FUN__text1__00847af0(param_1,param_2,0xfffffffc);
        return;
      }
      param_1[1] = local_48;
      (*(code *)param_2[9])(param_2[10],param_1[3]);
      *param_1 = 6;
    case 6:
      param_1[8] = local_10;
      param_1[7] = local_18;
      param_2[1] = local_20;
      param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
      *param_2 = (int)local_8;
      param_1[0xd] = local_c;
      iVar3 = FUN__text1__00846245(param_1,param_2,param_3);
      if (iVar3 != 1) {
        FUN__text1__00847af0(param_1,param_2,iVar3);
        return;
      }
      param_3 = 0;
      FUN__text1__00846f99(param_1[1],param_2);
      local_8 = (byte *)*param_2;
      local_20 = param_2[1];
      local_10 = param_1[8];
      local_18 = param_1[7];
      local_c = param_1[0xd];
      if (local_c < param_1[0xc]) {
        local_7c = (param_1[0xc] - local_c) - 1;
      }
      else {
        local_7c = param_1[0xb] - local_c;
      }
      local_1c = local_7c;
      if (param_1[6] != 0) {
        *param_1 = 7;
switchD__text1__00844e31_caseD_7:
        param_1[0xd] = local_c;
        uVar4 = FUN__text1__00847af0(param_1,param_2,param_3);
        local_c = param_1[0xd];
        if (local_c < param_1[0xc]) {
          local_80 = (param_1[0xc] - local_c) - 1;
        }
        else {
          local_80 = param_1[0xb] - local_c;
        }
        local_1c = local_80;
        if (param_1[0xc] != param_1[0xd]) {
          param_1[8] = local_10;
          param_1[7] = local_18;
          param_2[1] = local_20;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          param_1[0xd] = local_c;
          FUN__text1__00847af0(param_1,param_2,uVar4);
          return;
        }
        *param_1 = 8;
        goto switchD__text1__00844e31_caseD_8;
      }
      *param_1 = 0;
      break;
    case 7:
      goto switchD__text1__00844e31_caseD_7;
    case 8:
switchD__text1__00844e31_caseD_8:
      param_1[8] = local_10;
      param_1[7] = local_18;
      param_2[1] = local_20;
      param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
      *param_2 = (int)local_8;
      param_1[0xd] = local_c;
      FUN__text1__00847af0(param_1,param_2,1);
      return;
    case 9:
      param_1[8] = local_10;
      param_1[7] = local_18;
      param_2[1] = local_20;
      param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
      *param_2 = (int)local_8;
      param_1[0xd] = local_c;
      FUN__text1__00847af0(param_1,param_2,0xfffffffd);
      return;
    default:
      param_1[8] = local_10;
      param_1[7] = local_18;
      param_2[1] = local_20;
      param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
      *param_2 = (int)local_8;
      param_1[0xd] = local_c;
      FUN__text1__00847af0(param_1,param_2,0xfffffffe);
      return;
    }
  } while( true );
}

