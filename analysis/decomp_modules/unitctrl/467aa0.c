
void __thiscall FUN__text__00467aa0(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x2e6fc) = param_2;
  *(undefined4 *)(param_1 + 0x2e6f4) = param_2;
  *(undefined4 *)(param_1 + 0x2e6f8) = 0;
  *(int *)(param_1 + 0x2e700) = (*(int *)(param_1 + 0x2e6fc) % 0xc5c100) / 0x34bc0;
  *(int *)(param_1 + 0x2e704) = (*(int *)(param_1 + 0x2e6fc) % 0x34bc0) / 0xe10;
  *(int *)(param_1 + 0x2e708) = (*(int *)(param_1 + 0x2e6fc) % 0xe10) / 0x3c;
  return;
}

