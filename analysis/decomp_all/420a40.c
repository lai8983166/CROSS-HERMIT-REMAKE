
undefined4 FUN__text__00420a40(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [19];
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(short *)(param_1 + 0x1c) == 4) || (*(short *)(param_1 + 0x1c) == 8)) &&
     (*(int *)(param_1 + 0x2e) == 0)) {
    *(uint *)(param_1 + 0x2e) = *(int *)(param_1 + 10) - 0x36U >> 2;
  }
  return 0;
}

