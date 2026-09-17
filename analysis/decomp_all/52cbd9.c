
undefined4 __thiscall FUN__text__0052cbd9(int *param_1,int *param_2,int *param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  uint uVar5;
  int iVar6;
  int *piVar7;
  uint uVar8;
  int *piVar9;
  uint uVar10;
  uint uVar11;
  int *local_2c;
  uint local_24;
  int *local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  int *local_8;
  
  if (((param_3 < 4) || (*param_2 != 0x20534444)) || ((int)param_3 - 4U < 0x7c)) {
    return 0x80004005;
  }
  local_8 = param_2 + 0x20;
  param_1[3] = param_2[4];
  param_1[4] = param_2[3];
  if ((*(byte *)((int)param_2 + 10) & 0x80) == 0) {
    iVar1 = 1;
  }
  else {
    iVar1 = param_2[6];
  }
  param_1[5] = iVar1;
  if (iVar1 == 0) {
    param_1[5] = 1;
  }
  if ((param_2[0x1c] & 0xfc00U) == 0xfc00) {
    local_18 = 6;
  }
  else {
    if ((param_2[0x1c] & 0xfc00U) != 0) {
      return 0x80004005;
    }
    local_18 = 1;
  }
  local_24 = param_2[7];
  if (local_24 == 0) {
    local_24 = 1;
  }
  piVar9 = &DAT_0075de48;
  iVar1 = DAT_0075de48;
  while (iVar1 != 0) {
    if ((param_2[0x13] == 0x20) && (uVar10 = piVar9[2], param_2[0x14] == uVar10)) {
      if ((((((uVar10 & 4) == 0) || (param_2[0x15] == piVar9[3])) &&
           (((uVar10 & 0xc4462) == 0 || (param_2[0x16] == piVar9[4])))) &&
          (((uVar10 & 0xe4040) == 0 || (param_2[0x17] == piVar9[5])))) &&
         (((((uVar10 & 0xc4440) == 0 || (param_2[0x18] == piVar9[6])) &&
           (((uVar10 & 0xc4040) == 0 || (param_2[0x19] == piVar9[7])))) &&
          (((uVar10 & 0x80003) == 0 || (param_2[0x1a] == piVar9[8])))))) break;
    }
    piVar9 = piVar9 + 9;
    iVar1 = *piVar9;
  }
  iVar1 = *piVar9;
  if (iVar1 == 0) {
    return 0x80004005;
  }
  iVar2 = FUN__text__00526c46(iVar1);
  if ((*(byte *)((int)param_2 + 10) & 0x80) == 0) {
    param_1[0x11] = (uint)(local_18 == 6) * 2 + 3;
  }
  else {
    param_1[0x11] = 4;
  }
  if (*(int *)(iVar2 + 4) == 1) {
    if ((int *)((int)param_3 - 0x80U) < (int *)0x400) {
      return 0x80004005;
    }
    param_3 = (int *)((int)param_3 - 0x480);
    local_2c = local_8;
    local_8 = param_2 + 0x120;
  }
  else {
    local_2c = (int *)0x0;
    param_3 = (int *)((int)param_3 - 0x80U);
  }
  local_14 = 0;
  piVar9 = param_3;
  if (local_18 != 0) {
    do {
      uVar10 = param_1[3];
      uVar8 = param_1[4];
      param_2 = (int *)param_1[5];
      piVar4 = param_1;
      if (local_14 != 0) {
        iVar3 = FUN__text__00428a40(0x54);
        if (iVar3 == 0) {
          piVar4 = (int *)0x0;
        }
        else {
          piVar4 = (int *)FUN__text__0052b0a9();
        }
        if (piVar4 == (int *)0x0) {
          return 0x8007000e;
        }
        local_1c[0x14] = (int)piVar4;
      }
      local_10 = 0;
      piVar7 = piVar9;
      if (local_24 != 0) {
        do {
          piVar9 = piVar4;
          if (local_10 != 0) {
            iVar3 = FUN__text__00428a40(0x54);
            if (iVar3 == 0) {
              piVar9 = (int *)0x0;
            }
            else {
              piVar9 = (int *)FUN__text__0052b0a9();
            }
            if (piVar9 == (int *)0x0) {
              return 0x8007000e;
            }
            piVar7[0x13] = (int)piVar9;
          }
          if (iVar1 == 0x31545844) {
            iVar3 = (uVar10 + 3 >> 2) << 3;
LAB__text__0052ce76:
            iVar6 = (uVar8 + 3 >> 2) * iVar3;
          }
          else {
            if (iVar1 == 0x32545844) {
LAB__text__0052ce62:
              iVar3 = (uVar10 + 3 >> 2) << 4;
              goto LAB__text__0052ce76;
            }
            if (iVar1 == 0x32595559) {
LAB__text__0052ce53:
              iVar3 = (uVar10 + 1 >> 1) << 2;
            }
            else {
              if (((iVar1 == 0x33545844) || (iVar1 == 0x34545844)) || (iVar1 == 0x35545844))
              goto LAB__text__0052ce62;
              if (iVar1 == 0x59565955) goto LAB__text__0052ce53;
              iVar3 = (*(uint *)(iVar2 + 8) >> 3) * uVar10;
            }
            iVar6 = iVar3 * uVar8;
          }
          piVar9[0xe] = 0;
          piVar9[0xf] = 0;
          piVar7 = (int *)(iVar6 * (int)param_2);
          *piVar9 = iVar1;
          piVar9[0xc] = iVar3;
          piVar9[1] = (int)local_8;
          piVar9[5] = (int)param_2;
          piVar9[0xd] = iVar6;
          piVar9[3] = uVar10;
          piVar9[4] = uVar8;
          piVar9[2] = (int)local_2c;
          if (param_3 < piVar7) {
            return 0x80004005;
          }
          local_8 = (int *)((int)local_8 + (int)piVar7);
          param_3 = (int *)((int)param_3 - (int)piVar7);
          uVar5 = 1;
          uVar11 = uVar5;
          if (uVar10 != 1) {
            uVar11 = uVar10 >> 1;
          }
          if (uVar8 != 1) {
            uVar5 = uVar8 >> 1;
          }
          if (param_2 == (int *)0x1) {
            param_2 = (int *)0x1;
          }
          else {
            param_2 = (int *)((uint)param_2 >> 1);
          }
          local_10 = local_10 + 1;
          uVar8 = uVar5;
          piVar7 = piVar9;
          uVar10 = uVar11;
        } while (local_10 < local_24);
      }
      local_14 = local_14 + 1;
      local_1c = piVar4;
    } while (local_14 < local_18);
  }
  return 0;
}

