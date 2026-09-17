
void __thiscall
FUN__text__004558e0(int param_1,int param_2,undefined1 param_3,char param_4,undefined4 param_5)

{
  undefined1 *puVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [18];
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  puVar1 = (undefined1 *)(*(int *)(param_1 + 0x60) + 0x2170 + param_2 * 0xc);
  *puVar1 = 1;
  puVar1[1] = param_3;
  *(short *)(puVar1 + 2) = (short)param_4;
  *(undefined4 *)(puVar1 + 4) = param_5;
  *(undefined4 *)(puVar1 + 8) = param_5;
  return;
}

