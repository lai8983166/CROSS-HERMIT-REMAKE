
undefined2 __thiscall FUN__text__004c0060(int param_1,short param_2,short param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [19];
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  return *(undefined2 *)(param_1 + 0x136e + (short)(param_2 + param_3 * 0xc) * 2);
}

