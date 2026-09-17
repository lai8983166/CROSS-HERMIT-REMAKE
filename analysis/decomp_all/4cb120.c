
void __thiscall FUN__text__004cb120(int param_1,short param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 == -1) {
    *(undefined1 *)(param_1 + 0x14) = 0;
  }
  else {
    *(short *)(param_1 + 0xe) = param_2;
    *(undefined2 *)(param_1 + 0x12) = param_3;
    *(undefined1 *)(param_1 + 0x14) = 1;
  }
  return;
}

