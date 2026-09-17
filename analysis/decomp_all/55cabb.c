
void FUN__text__0055cabb(int *param_1,int param_2,int *param_3)

{
  int iVar1;
  
  if (param_3 != (int *)0x0) {
    *param_3 = param_1[0xf];
  }
  if ((*param_1 == 4) || (*param_1 == 5)) {
    (**(code **)(param_2 + 0x24))(*(undefined4 *)(param_2 + 0x28),param_1[3]);
  }
  if (*param_1 == 6) {
    FUN__text__00560010(param_1[1],param_2);
  }
  param_1[0xd] = param_1[10];
  param_1[0xc] = param_1[10];
  *param_1 = 0;
  param_1[7] = 0;
  param_1[8] = 0;
  if ((code *)param_1[0xe] != (code *)0x0) {
    iVar1 = (*(code *)param_1[0xe])(0,0,0);
    param_1[0xf] = iVar1;
    *(int *)(param_2 + 0x30) = iVar1;
  }
  return;
}

