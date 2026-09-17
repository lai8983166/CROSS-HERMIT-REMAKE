
undefined4 __thiscall FUN__text__0052cf1a(int *param_1,undefined4 param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  int *piVar6;
  int *piVar7;
  uint *puVar8;
  int *piVar9;
  uint uVar10;
  uint local_98 [5];
  uint local_84;
  int local_80;
  int local_50 [8];
  uint local_30;
  byte local_2b;
  byte local_2a;
  undefined4 local_1c;
  int *local_18;
  uint local_14;
  undefined1 local_10 [4];
  int *local_c;
  uint local_8;
  
  local_8 = 0;
  for (piVar6 = param_1; piVar6 != (int *)0x0; piVar6 = (int *)piVar6[0x13]) {
    local_8 = local_8 + 1;
  }
  piVar6 = &DAT_0075de48;
  if (DAT_0075de48 != 0) {
    iVar4 = DAT_0075de48;
    do {
      if (iVar4 == *param_1) break;
      piVar6 = piVar6 + 9;
      iVar4 = *piVar6;
    } while (iVar4 != 0);
  }
  if (*piVar6 == 0) {
    uVar2 = 0x80004005;
  }
  else {
    local_18 = param_1;
    local_c = (int *)FUN__text__00526c46(*param_1);
    local_14 = *(uint *)((int)local_c + 8) >> 3;
    local_1c = 0x20534444;
    (*DAT_005922bc)(param_2,&local_1c,4,local_10,0);
    pcVar1 = DAT_005922bc;
    puVar8 = local_98;
    for (iVar4 = 0x1f; iVar4 != 0; iVar4 = iVar4 + -1) {
      *puVar8 = 0;
      puVar8 = puVar8 + 1;
    }
    local_98[2] = param_1[4];
    local_98[3] = param_1[3];
    uVar3 = piVar6[2];
    local_98[0] = 0x7c;
    local_98[1] = 0x1007;
    piVar9 = local_50;
    for (iVar4 = 8; piVar7 = local_18, piVar6 = piVar6 + 1, iVar4 != 0; iVar4 = iVar4 + -1) {
      *piVar9 = *piVar6;
      piVar9 = piVar9 + 1;
    }
    local_30 = 0x1000;
    if ((uVar3 & 3) != 0) {
      local_30 = 0x1002;
    }
    if ((uVar3 & 0x20) != 0) {
      local_30 = local_30 | 0x100;
    }
    if (local_18[0x13] != 0) {
      local_30 = local_30 | 0x400008;
      local_98[1] = 0x21007;
      local_80 = local_8;
    }
    if (local_18[0x14] != 0) {
      local_30 = local_30 | 8;
      local_2b = local_2b | 0xfe;
    }
    if (1 < (uint)local_18[5]) {
      local_98[1] = local_98[1] | 0x800000;
      local_2a = local_2a | 0x20;
      local_84 = local_18[5];
    }
    (*DAT_005922bc)(param_2,local_98,0x7c,local_10,0);
    if (*(int *)((int)local_c + 4) == 1) {
      (*pcVar1)(param_2,piVar7[2],0x400,local_10,0);
    }
    local_c = piVar7;
    do {
      for (; piVar7 != (int *)0x0; piVar7 = (int *)piVar7[0x13]) {
        local_8 = 0;
        if (piVar7[5] != 0) {
          uVar3 = piVar7[4];
          do {
            uVar10 = 0;
            if (uVar3 != 0) {
              do {
                iVar4 = *local_18;
                if (iVar4 == 0x31545844) {
                  iVar4 = (piVar7[7] + uVar10 >> 2) * piVar7[0xc] +
                          (piVar7[10] + local_8) * piVar7[0xd] + ((uint)piVar7[6] >> 2) * 8;
                  iVar5 = (piVar7[3] + 3U >> 2) << 3;
LAB__text__0052d16a:
                  iVar4 = iVar4 + piVar7[1];
                  uVar10 = uVar10 + 3;
                }
                else {
                  if (iVar4 == 0x32545844) {
LAB__text__0052d10c:
                    iVar4 = (piVar7[7] + uVar10 >> 2) * piVar7[0xc] +
                            (piVar7[10] + local_8) * piVar7[0xd] + ((uint)piVar7[6] >> 2) * 0x10;
                    iVar5 = (piVar7[3] + 3U >> 2) << 4;
                    goto LAB__text__0052d16a;
                  }
                  if (iVar4 == 0x32595559) {
LAB__text__0052d0e0:
                    iVar4 = (piVar7[7] + uVar10) * piVar7[0xc] +
                            (piVar7[10] + local_8) * piVar7[0xd] + piVar7[6] * local_14 + piVar7[1];
                    iVar5 = (piVar7[3] + 1U >> 1) << 2;
                  }
                  else {
                    if (((iVar4 == 0x33545844) || (iVar4 == 0x34545844)) || (iVar4 == 0x35545844))
                    goto LAB__text__0052d10c;
                    if (iVar4 == 0x59565955) goto LAB__text__0052d0e0;
                    iVar4 = (piVar7[7] + uVar10) * piVar7[0xc] +
                            (piVar7[10] + local_8) * piVar7[0xd] + piVar7[6] * local_14 + piVar7[1];
                    iVar5 = piVar7[3] * local_14;
                  }
                }
                (*pcVar1)(param_2,iVar4,iVar5,local_10,0);
                uVar3 = piVar7[4];
                uVar10 = uVar10 + 1;
              } while (uVar10 < uVar3);
            }
            local_8 = local_8 + 1;
          } while (local_8 < (uint)piVar7[5]);
        }
      }
      piVar7 = (int *)local_c[0x14];
      local_c = piVar7;
    } while (piVar7 != (int *)0x0);
    uVar2 = 0;
  }
  return uVar2;
}

