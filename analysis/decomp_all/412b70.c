
void __thiscall FUN__text__00412b70(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [19];
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x880) = param_2;
  *(undefined4 *)(param_1 + 0x884) = param_3;
  *(undefined4 *)(param_1 + 0x888) = 0;
  *(undefined4 *)(param_1 + 0x88c) = 0;
  *(undefined4 *)(param_1 + 0x8a4) = param_2;
  *(undefined4 *)(param_1 + 0x8a8) = param_3;
  *(undefined4 *)(param_1 + 0x8ac) = 0;
  *(undefined4 *)(param_1 + 0x8b0) = 0;
  return;
}

