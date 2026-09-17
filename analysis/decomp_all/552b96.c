
void FUN__text__00552b96(int *param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  
  iVar1 = param_1[0x69];
  param_1[0x1d] = *(int *)(iVar1 + 0x10);
  param_1[0x1c] = *(int *)(iVar1 + 0x14);
  iVar3 = param_1[0x13];
  if (iVar3 == 0) {
    if (param_1[0x19] == 3) {
      *(code **)(iVar1 + 4) = FUN__text__00552765;
    }
    else {
      *(code **)(iVar1 + 4) = FUN__text__005526dd;
    }
  }
  else if (iVar3 == 1) {
    if (param_1[0x19] == 3) {
      *(code **)(iVar1 + 4) = FUN__text__005528dd;
    }
    else {
      *(code **)(iVar1 + 4) = FUN__text__005527f2;
    }
    *(undefined4 *)(iVar1 + 0x30) = 0;
    if (*(char *)(iVar1 + 0x1c) == '\0') {
      FUN__text__0055248b(param_1);
    }
    if (*(int *)(iVar1 + 0x34) == 0) {
      FUN__text__00552618();
    }
  }
  else if (iVar3 == 2) {
    *(undefined1 *)(iVar1 + 0x54) = 0;
    piVar2 = (int *)(iVar1 + 0x44);
    *(code **)(iVar1 + 4) = FUN__text__005529dc;
    if (*piVar2 == 0) {
      FUN__text__00552b60();
    }
    iVar1 = param_1[0x17];
    iVar3 = 0;
    if (0 < param_1[0x19]) {
      do {
        FUN__text__00549547(*piVar2,iVar1 * 2 + 4);
        iVar3 = iVar3 + 1;
        piVar2 = piVar2 + 1;
      } while (iVar3 < param_1[0x19]);
    }
  }
  else {
    *(undefined4 *)(*param_1 + 0x14) = 0x2f;
    (**(code **)*param_1)(param_1);
  }
  return;
}

