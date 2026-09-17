
int FUN__text__0053ce58(int param_1,int *param_2)

{
  int iVar1;
  int local_24 [6];
  int local_c;
  int local_8;
  
  if (param_2 == (int *)0x0) {
    iVar1 = -0x7789f794;
  }
  else if ((((*(int *)(param_1 + 0x460) == 0) &&
            ((**(code **)(*param_2 + 0x38))(param_2,0,local_24),
            local_24[0] == *(int *)(param_1 + 0x10))) && (local_c == *(int *)(param_1 + 0xc))) &&
          (local_8 == *(int *)(param_1 + 0xc))) {
    iVar1 = FUN__text__0053cbe5();
    if (-1 < iVar1) {
      *(int **)(param_1 + 0x34) = param_2;
      (**(code **)(*param_2 + 4))(param_2);
      *(undefined4 *)(param_1 + 0x460) = 1;
      iVar1 = 0;
    }
  }
  else {
    iVar1 = -0x7789f794;
  }
  return iVar1;
}

