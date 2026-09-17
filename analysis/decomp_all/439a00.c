
int FUN__text__00439a00(int param_1,int param_2)

{
  int *piVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [19];
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 4) != 0) {
    piVar1 = (int *)(param_2 + 8);
    for (param_2 = *(int *)(param_1 + 4); param_2 != 0; param_2 = *(int *)(param_2 + 4)) {
      if ((*(short *)(*(int *)(param_2 + 8) + 2) == *(short *)(*piVar1 + 2)) &&
         (*(short *)(*(int *)(param_2 + 8) + 4) == *(short *)(*piVar1 + 4))) {
        return param_2;
      }
    }
  }
  return 0;
}

