
void __thiscall
FUN__text__0045a0a0(int param_1,int param_2,undefined2 param_3,undefined2 param_4,undefined2 param_5
                   ,undefined2 param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_2 + 0x38) = param_5;
  *(undefined2 *)(param_2 + 0x3a) = param_6;
  *(undefined2 *)(param_2 + 0x78) = param_3;
  *(undefined2 *)(param_2 + 0x7a) = param_4;
  *(short *)(param_2 + 0x7c) = *(short *)(param_1 + 0xc4) + *(short *)(param_1 + 0x84);
  *(short *)(param_2 + 0x7e) = *(short *)(param_1 + 0xc6) + *(short *)(param_1 + 0x86);
  return;
}

