
undefined4 __thiscall FUN__text__00464d70(int param_1,undefined4 param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x44) = param_2;
  *(undefined2 *)(param_1 + 0x48) = param_3;
  *(undefined **)(param_1 + 0x4c) = (&PTR_DAT_0060e850)[*(short *)(param_1 + 0x48)];
  *(undefined **)(param_1 + 0x50) = (&PTR_DAT_0060f070)[*(short *)(param_1 + 0x48)];
  return 0;
}

