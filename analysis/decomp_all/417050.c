
void FUN__text__00417050(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x18) = *(undefined4 *)(param_1 + 0x10);
  *(undefined4 *)(param_1 + 0x1c) = *(undefined4 *)(param_1 + 0x14);
  return;
}

