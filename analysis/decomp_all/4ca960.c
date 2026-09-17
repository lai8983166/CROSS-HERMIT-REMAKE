
undefined4 __thiscall FUN__text__004ca960(int param_1,undefined2 param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 0x1e) = param_2;
  *(undefined2 *)(param_1 + 0x20) = param_3;
  return CONCAT31((int3)(CONCAT22((short)((uint)param_1 >> 0x10),param_3) >> 8),1);
}

