
void FUN__text__004e2d00(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(int *)(param_1 + 0x1c) = *(int *)(param_1 + 0x1c) % 10;
  *(int *)(param_1 + 0x20) = *(int *)(param_1 + 0x20) % 10;
  *(int *)(param_1 + 0x24) = *(int *)(param_1 + 0x24) % 10;
  FUN__text__004e2da0(*(undefined4 *)(param_1 + 0x1c));
  FUN__text__004e2e00(*(undefined4 *)(param_1 + 0x20));
  FUN__text__004e2e60(*(undefined4 *)(param_1 + 0x24));
  uStack_8 = 0x4e2d8e;
  FUN__text__0056ce80();
  return;
}

