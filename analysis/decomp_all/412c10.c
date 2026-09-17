
void __thiscall FUN__text__00412c10(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x8ec) = param_2;
  *(undefined4 *)(param_1 + 0x8f0) = param_3;
  *(undefined4 *)(param_1 + 0x8f4) = 0;
  *(undefined4 *)(param_1 + 0x8f8) = 0;
  return;
}

