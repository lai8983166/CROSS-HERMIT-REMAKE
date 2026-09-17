
int FUN__text__0053cec8(int param_1,int *param_2)

{
  int iVar1;
  int local_24 [2];
  uint local_1c;
  int local_c;
  int local_8;
  
  if (param_2 == (int *)0x0) {
    iVar1 = -0x7789f794;
  }
  else if (*(int *)(param_1 + 0x460) == 0) {
    (**(code **)(*param_2 + 0x38))(param_2,0,local_24);
    if (((local_24[0] == *(int *)(param_1 + 0x10)) && (local_c == *(int *)(param_1 + 0xc))) &&
       (local_8 == *(int *)(param_1 + 0xc))) {
      *(uint *)(param_1 + 0x48) = local_1c & 1;
      iVar1 = FUN__text__0053cbe5();
      if (-1 < iVar1) {
        *(int **)(param_1 + 0x38) = param_2;
        (**(code **)(*param_2 + 4))(param_2);
        *(undefined4 *)(param_1 + 0x3c) = 0;
        *(undefined4 *)(param_1 + 0x460) = 2;
        iVar1 = 0;
      }
    }
    else {
      iVar1 = -0x7789f794;
    }
  }
  else {
    iVar1 = -0x7fffbffb;
  }
  return iVar1;
}

