
undefined4 FUN__text__0053c97a(int param_1)

{
  int *piVar1;
  undefined4 uVar2;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  if (*(int *)(param_1 + 0x30) == 0) {
    uVar2 = 0x80004005;
  }
  else {
    (**(code **)(**(int **)(param_1 + 8) + 0x8c))(*(int **)(param_1 + 8));
    if (*(int *)(param_1 + 0x34) == 0) {
      local_14 = *(int *)(param_1 + 0x3c);
      local_10 = *(int *)(param_1 + 0x40);
      local_c = *(int *)(param_1 + 0x44) + local_14;
      local_8 = *(int *)(param_1 + 0x48) + local_10;
      (**(code **)(**(int **)(param_1 + 8) + 0x70))
                (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0x20),&local_14,1,
                 *(undefined4 *)(param_1 + 0x30),&local_14);
    }
    (**(code **)(**(int **)(param_1 + 8) + 0x7c))
              (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0x24),
               *(undefined4 *)(param_1 + 0x2c));
    (**(code **)(**(int **)(param_1 + 8) + 0xd8))
              (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0x38));
    piVar1 = *(int **)(param_1 + 0x24);
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 8))(piVar1);
      *(undefined4 *)(param_1 + 0x24) = 0;
    }
    piVar1 = *(int **)(param_1 + 0x2c);
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 8))(piVar1);
      *(undefined4 *)(param_1 + 0x2c) = 0;
    }
    piVar1 = *(int **)(param_1 + 0x30);
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 8))(piVar1);
      *(undefined4 *)(param_1 + 0x30) = 0;
    }
    uVar2 = 0;
  }
  return uVar2;
}

