
void __thiscall FUN__text__004998b0(int param_1,undefined1 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)(param_1 + 0x3099a) = param_2;
  *(undefined4 *)(param_1 + 0x309a0) = 0;
  *(undefined1 *)(param_1 + 0x30999) = 0;
  *(undefined1 *)(param_1 + 0x30998) = 1;
  return;
}

