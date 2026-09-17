
void FUN__text__00550b99(int *param_1)

{
  undefined4 *puVar1;
  int iVar2;
  int iVar3;
  bool bVar4;
  
  puVar1 = (undefined4 *)(**(code **)param_1[1])(param_1,1,0x18);
  param_1[0x68] = (int)puVar1;
  *puVar1 = &DAT__text__005505d4;
  iVar2 = param_1[9];
  if (iVar2 == 1) {
    bVar4 = param_1[8] == 1;
LAB__text__00550be8:
    if (!bVar4) {
LAB__text__00550bea:
      *(undefined4 *)(*param_1 + 0x14) = 8;
      (**(code **)*param_1)(param_1);
    }
  }
  else {
    if (1 < iVar2) {
      if (iVar2 < 4) {
        bVar4 = param_1[8] == 3;
      }
      else {
        if (5 < iVar2) goto LAB__text__00550bde;
        bVar4 = param_1[8] == 4;
      }
      goto LAB__text__00550be8;
    }
LAB__text__00550bde:
    if (param_1[8] < 1) goto LAB__text__00550bea;
  }
  iVar2 = param_1[10];
  if (iVar2 == 1) {
    iVar2 = 1;
    param_1[0x19] = 1;
    if ((param_1[9] == 1) || (param_1[9] == 3)) {
      puVar1[1] = FUN__text__0055047f;
      if (1 < param_1[8]) {
        iVar3 = 0x54;
        do {
          *(undefined1 *)(param_1[0x31] + 0x30 + iVar3) = 0;
          iVar2 = iVar2 + 1;
          iVar3 = iVar3 + 0x54;
        } while (iVar2 < param_1[8]);
      }
      goto LAB__text__00550ca1;
    }
  }
  else if (iVar2 == 2) {
    param_1[0x19] = 3;
    if (param_1[9] == 3) {
      puVar1[1] = FUN__text__0055097b;
      goto LAB__text__00550c54;
    }
    bVar4 = param_1[9] == 2;
LAB__text__00550c60:
    if (bVar4) goto LAB__text__00550c62;
  }
  else {
    if (iVar2 == 4) {
      param_1[0x19] = 4;
      if (param_1[9] != 5) {
        bVar4 = param_1[9] == 4;
        goto LAB__text__00550c60;
      }
      puVar1[1] = FUN__text__005504a2;
LAB__text__00550c54:
      FUN__text__00550364();
      goto LAB__text__00550ca1;
    }
    if (iVar2 == param_1[9]) {
      param_1[0x19] = param_1[8];
LAB__text__00550c62:
      puVar1[1] = FUN__text__00550414;
      goto LAB__text__00550ca1;
    }
  }
  *(undefined4 *)(*param_1 + 0x14) = 0x19;
  (**(code **)*param_1)(param_1);
LAB__text__00550ca1:
  if (*(char *)((int)param_1 + 0x4a) == '\0') {
    param_1[0x1a] = param_1[0x19];
  }
  else {
    param_1[0x1a] = 1;
  }
  return;
}

