
void FUN__text1__00846245(int param_1,int *param_2,int param_3)

{
  byte *pbVar1;
  byte bVar2;
  int *piVar3;
  undefined4 uVar4;
  uint uVar5;
  uint local_54;
  uint local_50;
  uint local_4c;
  uint local_48;
  uint local_44;
  uint local_40;
  uint local_3c;
  uint local_34;
  uint local_30;
  uint local_2c;
  uint local_28;
  undefined1 *local_20;
  uint local_10;
  undefined1 *local_c;
  byte *local_8;
  
  piVar3 = *(int **)(param_1 + 4);
  local_8 = (byte *)*param_2;
  local_30 = param_2[1];
  local_10 = *(uint *)(param_1 + 0x20);
  local_28 = *(uint *)(param_1 + 0x1c);
  local_c = *(undefined1 **)(param_1 + 0x34);
  if (local_c < *(undefined1 **)(param_1 + 0x30)) {
    local_34 = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
  }
  else {
    local_34 = *(int *)(param_1 + 0x2c) - (int)local_c;
  }
  local_2c = local_34;
LAB__text1__008462ae:
  do {
    switch(*piVar3) {
    case 0:
      if ((0x101 < local_2c) && (9 < local_30)) {
        *(uint *)(param_1 + 0x20) = local_10;
        *(uint *)(param_1 + 0x1c) = local_28;
        param_2[1] = local_30;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        *(undefined1 **)(param_1 + 0x34) = local_c;
        param_3 = FUN__text1__00847cd0
                            ((char)piVar3[4],*(undefined1 *)((int)piVar3 + 0x11),piVar3[5],piVar3[6]
                             ,param_1,param_2);
        local_8 = (byte *)*param_2;
        local_30 = param_2[1];
        local_10 = *(uint *)(param_1 + 0x20);
        local_28 = *(uint *)(param_1 + 0x1c);
        local_c = *(undefined1 **)(param_1 + 0x34);
        if (local_c < *(undefined1 **)(param_1 + 0x30)) {
          local_3c = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
        }
        else {
          local_3c = *(int *)(param_1 + 0x2c) - (int)local_c;
        }
        local_2c = local_3c;
        if (param_3 != 0) {
          *piVar3 = (-(uint)(param_3 != 1) & 2) + 7;
          break;
        }
      }
      piVar3[3] = (uint)*(byte *)(piVar3 + 4);
      piVar3[2] = piVar3[5];
      *piVar3 = 1;
    case 1:
      for (; local_28 < (uint)piVar3[3]; local_28 = local_28 + 8) {
        if (local_30 == 0) {
          *(uint *)(param_1 + 0x20) = local_10;
          *(uint *)(param_1 + 0x1c) = local_28;
          param_2[1] = 0;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          *(undefined1 **)(param_1 + 0x34) = local_c;
          FUN__text1__00847af0(param_1,param_2,param_3);
          return;
        }
        param_3 = 0;
        local_30 = local_30 - 1;
        local_10 = local_10 | (uint)*local_8 << ((byte)local_28 & 0x1f);
        local_8 = local_8 + 1;
      }
      pbVar1 = (byte *)(piVar3[2] + (local_10 & *(uint *)(&DAT_008701c8 + piVar3[3] * 4)) * 8);
      local_10 = local_10 >> (pbVar1[1] & 0x1f);
      local_28 = local_28 - pbVar1[1];
      bVar2 = *pbVar1;
      uVar5 = (uint)bVar2;
      if (uVar5 == 0) {
        piVar3[2] = *(int *)(pbVar1 + 4);
        *piVar3 = 6;
      }
      else if ((bVar2 & 0x10) == 0) {
        if ((bVar2 & 0x40) == 0) {
          piVar3[3] = uVar5;
          piVar3[2] = (int)(pbVar1 + *(int *)(pbVar1 + 4) * 8);
        }
        else {
          if ((bVar2 & 0x20) == 0) {
            *piVar3 = 9;
            param_2[6] = (int)"invalid literal/length code";
            *(uint *)(param_1 + 0x20) = local_10;
            *(uint *)(param_1 + 0x1c) = local_28;
            param_2[1] = local_30;
            param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
            *param_2 = (int)local_8;
            *(undefined1 **)(param_1 + 0x34) = local_c;
            FUN__text1__00847af0(param_1,param_2,0xfffffffd);
            return;
          }
          *piVar3 = 7;
        }
      }
      else {
        piVar3[2] = uVar5 & 0xf;
        piVar3[1] = *(int *)(pbVar1 + 4);
        *piVar3 = 2;
      }
      break;
    case 2:
      uVar5 = piVar3[2];
      for (; local_28 < uVar5; local_28 = local_28 + 8) {
        if (local_30 == 0) {
          *(uint *)(param_1 + 0x20) = local_10;
          *(uint *)(param_1 + 0x1c) = local_28;
          param_2[1] = 0;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          *(undefined1 **)(param_1 + 0x34) = local_c;
          FUN__text1__00847af0(param_1,param_2,param_3);
          return;
        }
        param_3 = 0;
        local_30 = local_30 - 1;
        local_10 = local_10 | (uint)*local_8 << ((byte)local_28 & 0x1f);
        local_8 = local_8 + 1;
      }
      piVar3[1] = piVar3[1] + (local_10 & *(uint *)(&DAT_008701c8 + uVar5 * 4));
      local_10 = local_10 >> ((byte)uVar5 & 0x1f);
      local_28 = local_28 - uVar5;
      piVar3[3] = (uint)*(byte *)((int)piVar3 + 0x11);
      piVar3[2] = piVar3[6];
      *piVar3 = 3;
    case 3:
      for (; local_28 < (uint)piVar3[3]; local_28 = local_28 + 8) {
        if (local_30 == 0) {
          *(uint *)(param_1 + 0x20) = local_10;
          *(uint *)(param_1 + 0x1c) = local_28;
          param_2[1] = 0;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          *(undefined1 **)(param_1 + 0x34) = local_c;
          FUN__text1__00847af0(param_1,param_2,param_3);
          return;
        }
        param_3 = 0;
        local_30 = local_30 - 1;
        local_10 = local_10 | (uint)*local_8 << ((byte)local_28 & 0x1f);
        local_8 = local_8 + 1;
      }
      pbVar1 = (byte *)(piVar3[2] + (local_10 & *(uint *)(&DAT_008701c8 + piVar3[3] * 4)) * 8);
      local_10 = local_10 >> (pbVar1[1] & 0x1f);
      local_28 = local_28 - pbVar1[1];
      bVar2 = *pbVar1;
      if ((bVar2 & 0x10) == 0) {
        if ((bVar2 & 0x40) != 0) {
          *piVar3 = 9;
          param_2[6] = (int)"invalid distance code";
          *(uint *)(param_1 + 0x20) = local_10;
          *(uint *)(param_1 + 0x1c) = local_28;
          param_2[1] = local_30;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          *(undefined1 **)(param_1 + 0x34) = local_c;
          FUN__text1__00847af0(param_1,param_2,0xfffffffd);
          return;
        }
        piVar3[3] = (uint)bVar2;
        piVar3[2] = (int)(pbVar1 + *(int *)(pbVar1 + 4) * 8);
      }
      else {
        piVar3[2] = bVar2 & 0xf;
        piVar3[3] = *(int *)(pbVar1 + 4);
        *piVar3 = 4;
      }
      break;
    case 4:
      uVar5 = piVar3[2];
      for (; local_28 < uVar5; local_28 = local_28 + 8) {
        if (local_30 == 0) {
          *(uint *)(param_1 + 0x20) = local_10;
          *(uint *)(param_1 + 0x1c) = local_28;
          param_2[1] = 0;
          param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
          *param_2 = (int)local_8;
          *(undefined1 **)(param_1 + 0x34) = local_c;
          FUN__text1__00847af0(param_1,param_2,param_3);
          return;
        }
        param_3 = 0;
        local_30 = local_30 - 1;
        local_10 = local_10 | (uint)*local_8 << ((byte)local_28 & 0x1f);
        local_8 = local_8 + 1;
      }
      piVar3[3] = piVar3[3] + (local_10 & *(uint *)(&DAT_008701c8 + uVar5 * 4));
      local_10 = local_10 >> ((byte)uVar5 & 0x1f);
      local_28 = local_28 - uVar5;
      *piVar3 = 5;
    case 5:
      for (local_20 = local_c + -piVar3[3]; local_20 < *(undefined1 **)(param_1 + 0x28);
          local_20 = local_20 + (*(int *)(param_1 + 0x2c) - *(int *)(param_1 + 0x28))) {
      }
      while (piVar3[1] != 0) {
        if (local_2c == 0) {
          if ((local_c == *(undefined1 **)(param_1 + 0x2c)) &&
             (*(int *)(param_1 + 0x30) != *(int *)(param_1 + 0x28))) {
            local_c = *(undefined1 **)(param_1 + 0x28);
            if (local_c < *(undefined1 **)(param_1 + 0x30)) {
              local_40 = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
            }
            else {
              local_40 = *(int *)(param_1 + 0x2c) - (int)local_c;
            }
            local_2c = local_40;
          }
          if (local_2c == 0) {
            *(undefined1 **)(param_1 + 0x34) = local_c;
            uVar4 = FUN__text1__00847af0(param_1,param_2,param_3);
            local_c = *(undefined1 **)(param_1 + 0x34);
            if (local_c < *(undefined1 **)(param_1 + 0x30)) {
              local_44 = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
            }
            else {
              local_44 = *(int *)(param_1 + 0x2c) - (int)local_c;
            }
            local_2c = local_44;
            if ((local_c == *(undefined1 **)(param_1 + 0x2c)) &&
               (*(int *)(param_1 + 0x30) != *(int *)(param_1 + 0x28))) {
              local_c = *(undefined1 **)(param_1 + 0x28);
              if (local_c < *(undefined1 **)(param_1 + 0x30)) {
                local_48 = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
              }
              else {
                local_48 = *(int *)(param_1 + 0x2c) - (int)local_c;
              }
              local_2c = local_48;
            }
            if (local_2c == 0) {
              *(uint *)(param_1 + 0x20) = local_10;
              *(uint *)(param_1 + 0x1c) = local_28;
              param_2[1] = local_30;
              param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
              *param_2 = (int)local_8;
              *(undefined1 **)(param_1 + 0x34) = local_c;
              FUN__text1__00847af0(param_1,param_2,uVar4);
              return;
            }
          }
        }
        param_3 = 0;
        *local_c = *local_20;
        local_c = local_c + 1;
        local_20 = local_20 + 1;
        local_2c = local_2c - 1;
        if (local_20 == *(undefined1 **)(param_1 + 0x2c)) {
          local_20 = *(undefined1 **)(param_1 + 0x28);
        }
        piVar3[1] = piVar3[1] + -1;
      }
      *piVar3 = 0;
      break;
    case 6:
      goto switchD__text1__008462d0_caseD_6;
    case 7:
      if (7 < local_28) {
        local_28 = local_28 - 8;
        local_30 = local_30 + 1;
        local_8 = local_8 + -1;
      }
      *(undefined1 **)(param_1 + 0x34) = local_c;
      uVar4 = FUN__text1__00847af0(param_1,param_2,param_3);
      local_c = *(undefined1 **)(param_1 + 0x34);
      if (*(int *)(param_1 + 0x30) == *(int *)(param_1 + 0x34)) {
        *piVar3 = 8;
switchD__text1__008462d0_caseD_8:
        *(uint *)(param_1 + 0x20) = local_10;
        *(uint *)(param_1 + 0x1c) = local_28;
        param_2[1] = local_30;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        *(undefined1 **)(param_1 + 0x34) = local_c;
        FUN__text1__00847af0(param_1,param_2,1);
      }
      else {
        *(uint *)(param_1 + 0x20) = local_10;
        *(uint *)(param_1 + 0x1c) = local_28;
        param_2[1] = local_30;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        *(undefined1 **)(param_1 + 0x34) = local_c;
        FUN__text1__00847af0(param_1,param_2,uVar4);
      }
      return;
    case 8:
      goto switchD__text1__008462d0_caseD_8;
    case 9:
      *(uint *)(param_1 + 0x20) = local_10;
      *(uint *)(param_1 + 0x1c) = local_28;
      param_2[1] = local_30;
      param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
      *param_2 = (int)local_8;
      *(undefined1 **)(param_1 + 0x34) = local_c;
      FUN__text1__00847af0(param_1,param_2,0xfffffffd);
      return;
    default:
      *(uint *)(param_1 + 0x20) = local_10;
      *(uint *)(param_1 + 0x1c) = local_28;
      param_2[1] = local_30;
      param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
      *param_2 = (int)local_8;
      *(undefined1 **)(param_1 + 0x34) = local_c;
      FUN__text1__00847af0(param_1,param_2,0xfffffffe);
      return;
    }
  } while( true );
switchD__text1__008462d0_caseD_6:
  if (local_2c == 0) {
    if ((local_c == *(undefined1 **)(param_1 + 0x2c)) &&
       (*(int *)(param_1 + 0x30) != *(int *)(param_1 + 0x28))) {
      local_c = *(undefined1 **)(param_1 + 0x28);
      if (local_c < *(undefined1 **)(param_1 + 0x30)) {
        local_4c = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
      }
      else {
        local_4c = *(int *)(param_1 + 0x2c) - (int)local_c;
      }
      local_2c = local_4c;
    }
    if (local_2c == 0) {
      *(undefined1 **)(param_1 + 0x34) = local_c;
      uVar4 = FUN__text1__00847af0(param_1,param_2,param_3);
      local_c = *(undefined1 **)(param_1 + 0x34);
      if (local_c < *(undefined1 **)(param_1 + 0x30)) {
        local_50 = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
      }
      else {
        local_50 = *(int *)(param_1 + 0x2c) - (int)local_c;
      }
      local_2c = local_50;
      if ((local_c == *(undefined1 **)(param_1 + 0x2c)) &&
         (*(int *)(param_1 + 0x30) != *(int *)(param_1 + 0x28))) {
        local_c = *(undefined1 **)(param_1 + 0x28);
        if (local_c < *(undefined1 **)(param_1 + 0x30)) {
          local_54 = (*(int *)(param_1 + 0x30) - (int)local_c) - 1;
        }
        else {
          local_54 = *(int *)(param_1 + 0x2c) - (int)local_c;
        }
        local_2c = local_54;
      }
      if (local_2c == 0) {
        *(uint *)(param_1 + 0x20) = local_10;
        *(uint *)(param_1 + 0x1c) = local_28;
        param_2[1] = local_30;
        param_2[2] = (int)(local_8 + (param_2[2] - *param_2));
        *param_2 = (int)local_8;
        *(undefined1 **)(param_1 + 0x34) = local_c;
        FUN__text1__00847af0(param_1,param_2,uVar4);
        return;
      }
    }
  }
  param_3 = 0;
  *local_c = (char)piVar3[2];
  local_c = local_c + 1;
  local_2c = local_2c - 1;
  *piVar3 = 0;
  goto LAB__text1__008462ae;
}

