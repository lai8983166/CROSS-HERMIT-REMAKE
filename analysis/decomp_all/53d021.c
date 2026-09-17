
int FUN__text__0053d021(int param_1,int *param_2,int *param_3)

{
  int *piVar1;
  int iVar2;
  int local_24 [2];
  uint local_1c;
  int local_c;
  int local_8;
  
  if ((param_2 == (int *)0x0) && (param_3 == (int *)0x0)) {
    return -0x7789f794;
  }
  if (*(int *)(param_1 + 0x460) != 0) {
    return -0x7fffbffb;
  }
  if (param_2 == (int *)0x0) {
LAB__text__0053d08d:
    if (param_3 != (int *)0x0) {
      (**(code **)(*param_3 + 0x38))(param_3,0,local_24);
      if (((local_24[0] != *(int *)(param_1 + 0x10)) || (local_c != *(int *)(param_1 + 0xc))) ||
         (local_8 != *(int *)(param_1 + 0xc))) goto LAB__text__0053d070;
      *(uint *)(param_1 + 0x4c) = local_1c & 1;
    }
    iVar2 = FUN__text__0053cbe5();
    if (-1 < iVar2) {
      *(int **)(param_1 + 0x38) = param_2;
      *(int **)(param_1 + 0x3c) = param_3;
      if (param_2 != (int *)0x0) {
        (**(code **)(*param_2 + 4))(param_2);
      }
      piVar1 = *(int **)(param_1 + 0x3c);
      if (piVar1 != (int *)0x0) {
        (**(code **)(*piVar1 + 4))(piVar1);
      }
      *(undefined4 *)(param_1 + 0x460) = 4;
      iVar2 = 0;
    }
  }
  else {
    (**(code **)(*param_2 + 0x38))(param_2,0,local_24);
    if (((local_24[0] == *(int *)(param_1 + 0x10)) && (local_c == *(int *)(param_1 + 0xc))) &&
       (local_8 == *(int *)(param_1 + 0xc))) {
      *(uint *)(param_1 + 0x48) = local_1c & 1;
      goto LAB__text__0053d08d;
    }
LAB__text__0053d070:
    iVar2 = -0x7789f794;
  }
  return iVar2;
}

