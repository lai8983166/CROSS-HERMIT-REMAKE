
void FUN__text__004b9270(undefined2 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [16];
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(&DAT_007a4aec + DAT_007a4ae8 * 2) = param_1;
  DAT_007a4ae8 = DAT_007a4ae8 + 1;
  return;
}

