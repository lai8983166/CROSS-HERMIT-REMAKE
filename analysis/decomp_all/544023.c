
void FUN__text__00544023(int param_1,undefined4 *param_2)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_8;
  
  local_8 = FUN__text__0054458b(param_1);
  iVar1 = *(int *)(param_1 + 0xbc);
  *(int *)(param_1 + 0xc0) = iVar1;
  iVar2 = iVar1;
  puVar3 = param_2;
  if (0 < local_8) {
    do {
      for (; iVar2 != 0; iVar2 = iVar2 + -1) {
        FUN__text__00543c02(param_1,*puVar3,0);
        puVar3 = puVar3 + 1;
      }
      local_8 = local_8 + -1;
      iVar2 = iVar1;
      puVar3 = param_2;
    } while (local_8 != 0);
  }
  return;
}

