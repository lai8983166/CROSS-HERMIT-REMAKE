
void __thiscall FUN__text__00410930(int param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x40) = 1;
  *(undefined4 *)(param_1 + 0x44) = 1;
  *(int *)(param_1 + 0x48) = param_2;
  *(undefined4 *)(param_1 + 0x50) = param_3;
  *(undefined4 *)(param_1 + 0x54) = 0;
  *(undefined4 *)(param_1 + 0x5c) = 0xff0000;
  *(int *)(param_1 + 0x5c) = *(int *)(param_1 + 0x5c) / *(int *)(param_1 + 0x50);
  *(undefined4 *)(param_1 + 0x4c) = param_4;
  if (param_2 == 0) {
    *(undefined4 *)(param_1 + 0x58) = 0xff0000;
    *(int *)(param_1 + 0x5c) = -*(int *)(param_1 + 0x5c);
  }
  else {
    *(undefined4 *)(param_1 + 0x58) = 0;
  }
  return;
}

