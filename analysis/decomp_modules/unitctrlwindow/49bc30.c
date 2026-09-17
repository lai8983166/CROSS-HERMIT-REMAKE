
void FUN__text__0049bc30(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(byte *)(*(int *)(param_1 + 600) + 0x9d) = *(byte *)(*(int *)(param_1 + 600) + 0x9d) ^ 1;
  return;
}

