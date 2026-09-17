
void FUN__text__004dcf00(int param_1,undefined4 param_2,short *param_3,int param_4)

{
  int iVar1;
  short *psVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  short local_28;
  short local_26;
  short local_24;
  short local_22;
  short local_20;
  short local_1e;
  short local_1c;
  short local_1a;
  short local_18;
  short local_16;
  short local_14;
  short local_12;
  short local_10;
  short local_e;
  short local_c;
  short local_a;
  int local_8;
  
  puVar3 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 != 0) && (param_1 != 0xffff)) {
    _memset(&local_28,0,0x24);
    if (*(int *)(&DAT_00738998 + param_1 * 4) != 0) {
      (**(code **)(&DAT_00738998 + param_1 * 4))(param_2,&local_28);
      FUN__text__0056ce80();
    }
    local_10 = *(short *)(&DAT_006c2dd0 + param_1 * 0x48);
    if (param_4 == 0) {
      if ((int)*param_3 + (int)local_28 < 32000) {
        if ((int)*param_3 + (int)local_28 < -32000) {
          *param_3 = -32000;
        }
        else {
          *param_3 = *param_3 + local_28;
        }
      }
      else {
        *param_3 = 32000;
      }
      if ((int)param_3[1] + (int)local_26 < 32000) {
        if ((int)param_3[1] + (int)local_26 < -32000) {
          param_3[1] = -32000;
        }
        else {
          param_3[1] = param_3[1] + local_26;
        }
      }
      else {
        param_3[1] = 32000;
      }
      if ((int)param_3[2] + (int)local_24 < 32000) {
        if ((int)param_3[2] + (int)local_24 < -32000) {
          param_3[2] = -32000;
        }
        else {
          param_3[2] = param_3[2] + local_24;
        }
      }
      else {
        param_3[2] = 32000;
      }
      if ((int)param_3[3] + (int)local_22 < 32000) {
        if ((int)param_3[3] + (int)local_22 < -32000) {
          param_3[3] = -32000;
        }
        else {
          param_3[3] = param_3[3] + local_22;
        }
      }
      else {
        param_3[3] = 32000;
      }
      if ((int)param_3[5] + (int)local_1e < 32000) {
        if ((int)param_3[5] + (int)local_1e < -32000) {
          param_3[5] = -32000;
        }
        else {
          param_3[5] = param_3[5] + local_1e;
        }
      }
      else {
        param_3[5] = 32000;
      }
      if ((int)param_3[4] + (int)local_20 < 32000) {
        if ((int)param_3[4] + (int)local_20 < -32000) {
          param_3[4] = -32000;
        }
        else {
          param_3[4] = param_3[4] + local_20;
        }
      }
      else {
        param_3[4] = 32000;
      }
      if ((int)param_3[6] + (int)local_1c < 32000) {
        if ((int)param_3[6] + (int)local_1c < -32000) {
          param_3[6] = -32000;
        }
        else {
          param_3[6] = param_3[6] + local_1c;
        }
      }
      else {
        param_3[6] = 32000;
      }
      if ((int)param_3[7] + (int)local_1a < 32000) {
        if ((int)param_3[7] + (int)local_1a < -32000) {
          param_3[7] = -32000;
        }
        else {
          param_3[7] = param_3[7] + local_1a;
        }
      }
      else {
        param_3[7] = 32000;
      }
      if ((int)param_3[8] + (int)local_18 < 32000) {
        if ((int)param_3[8] + (int)local_18 < -32000) {
          param_3[8] = -32000;
        }
        else {
          param_3[8] = param_3[8] + local_18;
        }
      }
      else {
        param_3[8] = 32000;
      }
      if ((int)param_3[9] + (int)local_16 < 32000) {
        if ((int)param_3[9] + (int)local_16 < -32000) {
          param_3[9] = -32000;
        }
        else {
          param_3[9] = param_3[9] + local_16;
        }
      }
      else {
        param_3[9] = 32000;
      }
      if ((int)param_3[10] + (int)local_14 < 32000) {
        if ((int)param_3[10] + (int)local_14 < -32000) {
          param_3[10] = -32000;
        }
        else {
          param_3[10] = param_3[10] + local_14;
        }
      }
      else {
        param_3[10] = 32000;
      }
      if ((int)param_3[0xb] + (int)local_12 < 32000) {
        if ((int)param_3[0xb] + (int)local_12 < -32000) {
          param_3[0xb] = -32000;
        }
        else {
          param_3[0xb] = param_3[0xb] + local_12;
        }
      }
      else {
        param_3[0xb] = 32000;
      }
      if ((int)param_3[0xc] + (int)local_10 < 32000) {
        if ((int)param_3[0xc] + (int)local_10 < -32000) {
          param_3[0xc] = -32000;
        }
        else {
          param_3[0xc] = param_3[0xc] + local_10;
        }
      }
      else {
        param_3[0xc] = 32000;
      }
      if ((int)param_3[0xd] + (int)local_e < 32000) {
        if ((int)param_3[0xd] + (int)local_e < -32000) {
          param_3[0xd] = -32000;
        }
        else {
          param_3[0xd] = param_3[0xd] + local_e;
        }
      }
      else {
        param_3[0xd] = 32000;
      }
      if ((int)param_3[0xe] + (int)local_c < 32000) {
        if ((int)param_3[0xe] + (int)local_c < -32000) {
          param_3[0xe] = -32000;
        }
        else {
          param_3[0xe] = param_3[0xe] + local_c;
        }
      }
      else {
        param_3[0xe] = 32000;
      }
      if ((int)param_3[0xf] + (int)local_a < 32000) {
        if ((int)param_3[0xf] + (int)local_a < -32000) {
          param_3[0xf] = -32000;
        }
        else {
          param_3[0xf] = param_3[0xf] + local_a;
        }
      }
      else {
        param_3[0xf] = 32000;
      }
      if (*(int *)(param_3 + 0x10) + local_8 < 0x7fffffff) {
        if (*(int *)(param_3 + 0x10) + local_8 < -0x7fffffd0) {
          param_3[0x10] = 0x30;
          param_3[0x11] = -0x8000;
        }
        else {
          *(int *)(param_3 + 0x10) = *(int *)(param_3 + 0x10) + local_8;
        }
      }
      else {
        param_3[0x10] = -1;
        param_3[0x11] = 0x7fff;
      }
    }
    else {
      _memset(param_3,0,0x24);
      psVar2 = &local_28;
      for (iVar1 = 9; iVar1 != 0; iVar1 = iVar1 + -1) {
        *(undefined4 *)param_3 = *(undefined4 *)psVar2;
        psVar2 = psVar2 + 2;
        param_3 = param_3 + 2;
      }
    }
  }
  local_8 = 0x4dd505;
  FUN__text__0056ce80();
  return;
}

