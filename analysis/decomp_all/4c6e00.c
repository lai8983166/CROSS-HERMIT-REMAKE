
undefined4 __thiscall FUN__text__004c6e00(int param_1,undefined2 param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 4) = param_2;
  *(undefined2 *)(param_1 + 6) = param_3;
  return CONCAT31((int3)(CONCAT22((short)((uint)param_1 >> 0x10),param_3) >> 8),1);
}

