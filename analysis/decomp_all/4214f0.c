
int FUN__text__004214f0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 < *(int *)(param_1 + 4)) {
    param_1 = param_1 + *(int *)(param_1 + 8 + param_2 * 4);
  }
  else {
    param_1 = 0;
  }
  return param_1;
}

