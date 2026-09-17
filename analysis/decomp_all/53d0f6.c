
undefined4 FUN__text__0053d0f6(int param_1)

{
  int *piVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  
  piVar3 = *(int **)(param_1 + 8);
  if (piVar3 != (int *)0x0) {
    iVar2 = *(int *)(param_1 + 0x470);
    if (iVar2 != 0) {
      (**(code **)(*piVar3 + 0xe0))(piVar3,iVar2);
      *(int *)(param_1 + 0x470) = 0;
    }
    iVar2 = *(int *)(param_1 + 0x48c);
    if (iVar2 != 0) {
      (**(code **)(**(int **)(param_1 + 8) + 0xe0))(*(int **)(param_1 + 8),iVar2);
      *(int *)(param_1 + 0x48c) = 0;
    }
    iVar2 = *(int *)(param_1 + 0x490);
    if (iVar2 != 0) {
      (**(code **)(**(int **)(param_1 + 8) + 0xe0))(*(int **)(param_1 + 8),iVar2);
      *(int *)(param_1 + 0x490) = 0;
    }
  }
  piVar3 = *(int **)(param_1 + 0x20);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 0x20) = 0;
  }
  piVar3 = *(int **)(param_1 + 0x24);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 0x24) = 0;
  }
  piVar3 = *(int **)(param_1 + 0x28);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 0x28) = 0;
  }
  piVar3 = *(int **)(param_1 + 0x2c);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 0x2c) = 0;
  }
  piVar3 = *(int **)(param_1 + 0x34);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 0x34) = 0;
  }
  piVar3 = *(int **)(param_1 + 0x30);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))(piVar3);
    *(undefined4 *)(param_1 + 0x30) = 0;
  }
  piVar3 = (int *)(param_1 + 0x40);
  iVar2 = 2;
  do {
    piVar1 = (int *)piVar3[-2];
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 8))(piVar1);
      piVar3[-2] = 0;
    }
    piVar1 = (int *)*piVar3;
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 8))(piVar1);
      *piVar3 = 0;
    }
    piVar3 = piVar3 + 1;
    iVar2 = iVar2 + -1;
  } while (iVar2 != 0);
  piVar3 = (int *)(param_1 + 0x54);
  iVar2 = 5;
  do {
    iVar4 = 2;
    do {
      piVar1 = (int *)piVar3[-1];
      if (piVar1 != (int *)0x0) {
        (**(code **)(*piVar1 + 8))(piVar1);
        piVar3[-1] = 0;
      }
      piVar1 = (int *)*piVar3;
      if (piVar1 != (int *)0x0) {
        (**(code **)(*piVar1 + 8))(piVar1);
        *piVar3 = 0;
      }
      piVar3 = piVar3 + 0x1a;
      iVar4 = iVar4 + -1;
    } while (iVar4 != 0);
    iVar2 = iVar2 + -1;
  } while (iVar2 != 0);
  return 0;
}

