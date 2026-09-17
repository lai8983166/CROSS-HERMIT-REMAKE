
undefined4 FUN__text__00428070(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1;
  do {
    if (local_c == param_2) {
      return 1;
    }
    local_c = *(int *)(param_1 + 4);
  } while (local_c != 0);
  return 0;
}

