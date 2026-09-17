
void FUN__text__0054a5bc(int *param_1)

{
  uint uVar1;
  int *piVar2;
  char cVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  int local_8;
  
  piVar2 = param_1;
  if (param_1[4] != 0xca) {
    *(undefined4 *)(*param_1 + 0x14) = 0x12;
    *(int *)(*param_1 + 0x18) = param_1[4];
    (**(code **)*param_1)(param_1);
  }
  iVar4 = param_1[0xb];
  uVar1 = param_1[0xc];
  if (uVar1 < (uint)(iVar4 << 3)) {
    if (uVar1 < (uint)(iVar4 << 2)) {
      if (uVar1 < (uint)(iVar4 * 2)) {
        param_1[0x17] = param_1[6];
        iVar4 = param_1[7];
        param_1[0x45] = 8;
      }
      else {
        iVar4 = FUN__text__005494b6(param_1[6],2);
        param_1[0x17] = iVar4;
        iVar4 = FUN__text__005494b6(param_1[7],2);
        param_1[0x45] = 4;
      }
    }
    else {
      iVar4 = FUN__text__005494b6(param_1[6],4);
      param_1[0x17] = iVar4;
      iVar4 = FUN__text__005494b6(param_1[7],4);
      param_1[0x45] = 2;
    }
  }
  else {
    iVar4 = FUN__text__005494b6(param_1[6],8);
    param_1[0x17] = iVar4;
    iVar4 = FUN__text__005494b6(param_1[7],8);
    param_1[0x45] = 1;
  }
  local_8 = 0;
  param_1[0x18] = iVar4;
  if (0 < param_1[8]) {
    piVar5 = (int *)(param_1[0x31] + 0xc);
    do {
      iVar4 = piVar2[0x45];
      param_1 = (int *)iVar4;
      if (iVar4 < 8) {
        do {
          iVar6 = piVar5[-1] * (int)param_1 * 2;
          if ((iVar6 - piVar2[0x43] * iVar4 != 0 && piVar2[0x43] * iVar4 <= iVar6) ||
             (iVar6 = *piVar5 * (int)param_1 * 2,
             iVar6 - piVar2[0x44] * iVar4 != 0 && piVar2[0x44] * iVar4 <= iVar6)) break;
          param_1 = (int *)((int)param_1 * 2);
        } while ((int)param_1 < 8);
      }
      local_8 = local_8 + 1;
      piVar5[6] = (int)param_1;
      piVar5 = piVar5 + 0x15;
    } while (local_8 < piVar2[8]);
  }
  iVar4 = 0;
  if (0 < piVar2[8]) {
    piVar5 = (int *)(piVar2[0x31] + 0x24);
    do {
      iVar6 = FUN__text__005494b6(piVar5[-7] * *piVar5 * piVar2[6],piVar2[0x43] << 3);
      piVar5[1] = iVar6;
      iVar6 = FUN__text__005494b6(piVar5[-6] * piVar2[7] * *piVar5,piVar2[0x44] << 3);
      piVar5[2] = iVar6;
      iVar4 = iVar4 + 1;
      piVar5 = piVar5 + 0x15;
    } while (iVar4 < piVar2[8]);
  }
  iVar4 = piVar2[10];
  iVar6 = 1;
  if (iVar4 == 1) {
LAB__text__0054a777:
    piVar2[0x19] = iVar6;
  }
  else {
    if (1 < iVar4) {
      iVar6 = 3;
      if (iVar4 < 4) goto LAB__text__0054a777;
      if (iVar4 < 6) {
        piVar2[0x19] = 4;
        goto LAB__text__0054a77a;
      }
    }
    piVar2[0x19] = piVar2[8];
  }
LAB__text__0054a77a:
  if (*(char *)((int)piVar2 + 0x4a) == '\0') {
    iVar4 = piVar2[0x19];
  }
  else {
    iVar4 = 1;
  }
  piVar2[0x1a] = iVar4;
  cVar3 = FUN__text__0054a54b();
  if (cVar3 == '\0') {
    piVar2[0x1b] = 1;
  }
  else {
    piVar2[0x1b] = piVar2[0x44];
  }
  return;
}

