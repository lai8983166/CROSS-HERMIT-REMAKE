
int FUN__text__004cd700(int *param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [20];
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 - 1U < param_2) {
    param_2 = *param_1 - 1;
  }
  return (int)param_1 + param_1[param_2 + 1];
}

