
int __thiscall FUN__text__0043c0c0(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 < 0) {
    iVar1 = 10;
  }
  else if (param_3 < 0) {
    iVar1 = 10;
  }
  else if (param_2 < *(short *)(*(int *)(param_1 + 0x2659c) + 4)) {
    if (param_3 < *(short *)(*(int *)(param_1 + 0x2659c) + 6)) {
      iVar1 = (int)*(char *)(**(int **)(param_1 + 0x265a0) + 1 +
                            (param_3 * *(short *)(*(int *)(param_1 + 0x2659c) + 4) + param_2) * 2);
    }
    else {
      iVar1 = 10;
    }
  }
  else {
    iVar1 = 10;
  }
  return iVar1;
}

