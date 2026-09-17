
undefined4 __thiscall FUN__text__004c2610(int param_1,int param_2,int param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 0x24 + param_2 * 0x1c8) = 0;
  *(undefined4 *)(param_1 + 0x1c + param_2 * 0x1c8) = *(undefined4 *)(param_3 + 4);
  return param_4;
}

