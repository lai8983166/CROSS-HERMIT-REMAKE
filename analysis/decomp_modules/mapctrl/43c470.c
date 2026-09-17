
void __thiscall FUN__text__0043c470(int param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(int *)(param_1 + 0x265a0) != 0) && (param_2 != 0xff)) && (param_3 != 0xff)) {
    param_2 = param_3 * *(short *)(*(int *)(param_1 + 0x2659c) + 4) + param_2;
    if (param_4 == 0) {
      *(char *)(**(int **)(param_1 + 0x265a0) + 1 + param_2 * 2) =
           *(char *)(**(int **)(param_1 + 0x265a0) + 1 + param_2 * 2) + -1;
    }
    else {
      *(char *)(**(int **)(param_1 + 0x265a0) + 1 + param_2 * 2) =
           *(char *)(**(int **)(param_1 + 0x265a0) + 1 + param_2 * 2) + '\x01';
    }
  }
  return;
}

