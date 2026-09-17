
void FUN__text__00427a80(int *param_1)

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
  iVar2 = *param_1;
  piVar1 = (int *)param_1[1];
  if (iVar2 != 0) {
    *(int **)(iVar2 + 4) = piVar1;
  }
  if (piVar1 != (int *)0x0) {
    *piVar1 = iVar2;
  }
  return;
}

