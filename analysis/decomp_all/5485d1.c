
undefined4 __fastcall FUN__text__005485d1(int param_1)

{
  int *piVar1;
  int iVar2;
  int *piVar3;
  
  piVar3 = *(int **)(param_1 + 4);
  if (piVar3 != (int *)0x0) {
    if (*(int *)(param_1 + 100) != 0) {
      (**(code **)(*piVar3 + 0xe0))(piVar3,*(int *)(param_1 + 100));
      *(undefined4 *)(param_1 + 100) = 0;
    }
    if (*(int *)(param_1 + 0x68) != 0) {
      (**(code **)(**(int **)(param_1 + 4) + 0xe0))(*(int **)(param_1 + 4),*(int *)(param_1 + 0x68))
      ;
      *(undefined4 *)(param_1 + 0x68) = 0;
    }
  }
  piVar3 = *(int **)(param_1 + 0xc);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 0x20))(piVar3);
  }
  if (*(int *)(param_1 + 0x50) != 0) {
    piVar3 = (int *)(param_1 + 0x10);
    iVar2 = 8;
    do {
      piVar1 = (int *)piVar3[8];
      if (piVar1 != (int *)0x0) {
        (**(code **)(*piVar1 + 8))(piVar1);
        piVar3[8] = 0;
      }
      piVar1 = (int *)*piVar3;
      if (piVar1 != (int *)0x0) {
        (**(code **)(*piVar1 + 8))(piVar1);
        *piVar3 = 0;
      }
      piVar3 = piVar3 + 1;
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
  }
  return 0;
}

