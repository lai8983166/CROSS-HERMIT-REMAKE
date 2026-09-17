
void __thiscall
FUN__text__00456340(int param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4,
                   undefined1 param_5,char param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = *(int *)(param_1 + 0x60);
  *(undefined1 *)(iVar1 + 0x2434) = 1;
  *(undefined1 *)(iVar1 + 0x2435) = param_5;
  *(short *)(iVar1 + 0x2438) = (short)param_6;
  *(undefined2 *)(iVar1 + 0x243c) = param_2;
  *(undefined2 *)(iVar1 + 0x243e) = param_3;
  *(undefined2 *)(iVar1 + 0x2440) = 0;
  *(undefined2 *)(iVar1 + 0x2442) = 0;
  *(undefined2 *)(iVar1 + 0x2444) = param_4;
  *(undefined4 *)(iVar1 + 0x2448) = 0;
  return;
}

