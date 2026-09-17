
void FUN__text__004753f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x2a6) == '\0') {
    *(undefined4 *)(param_1 + 0x29b) = *(undefined4 *)(param_1 + 0x290);
    *(undefined4 *)(param_1 + 0x29f) = *(undefined4 *)(param_1 + 0x294);
    *(undefined2 *)(param_1 + 0x2a3) = *(undefined2 *)(param_1 + 0x298);
    *(undefined1 *)(param_1 + 0x2a5) = *(undefined1 *)(param_1 + 0x29a);
    *(undefined1 *)(param_1 + 0x2a6) = 1;
  }
  return;
}

