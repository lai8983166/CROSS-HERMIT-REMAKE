
undefined4 __thiscall
FUN__text__004c1e20(int param_1,int param_2,undefined2 param_3,undefined2 param_4,undefined2 param_5
                   ,undefined4 param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)(param_1 + 0x1cd) = 1;
  *(undefined2 *)(param_1 + 0x26 + param_2 * 0x1c8) = param_3;
  *(undefined2 *)(param_1 + 0x28 + param_2 * 0x1c8) = param_4;
  *(undefined2 *)(param_1 + 0x2a + param_2 * 0x1c8) = param_5;
  *(undefined4 *)(param_1 + 0x2c + param_2 * 0x1c8) = param_6;
  return 1;
}

