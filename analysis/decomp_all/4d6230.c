
undefined2 __thiscall FUN__text__004d6230(int param_1,undefined2 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(param_2) {
  case 0:
    if (*(short *)(param_1 + 4) != 0) {
      *(short *)(param_1 + 4) = *(short *)(param_1 + 4) + -1;
    }
    break;
  case 1:
    if (*(short *)(param_1 + 4) != *(short *)(param_1 + 6)) {
      *(short *)(param_1 + 4) = *(short *)(param_1 + 4) + 1;
    }
    break;
  case 2:
    *(undefined2 *)(param_1 + 4) = 0;
    break;
  case 3:
    *(undefined2 *)(param_1 + 4) = *(undefined2 *)(param_1 + 6);
  }
  return *(undefined2 *)(param_1 + 4);
}

