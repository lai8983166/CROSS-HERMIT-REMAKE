
void FUN__text__0046b2c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)(param_1 + 0x4e9) = *(undefined1 *)(param_1 + 0x4e7);
  *(undefined1 *)(param_1 + 0x4ea) = *(undefined1 *)(param_1 + 0x4e8);
  *(char *)(param_1 + 0x4e7) =
       (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                   (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  *(char *)(param_1 + 0x4e8) =
       (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)
                   ) >> 4);
  return;
}

