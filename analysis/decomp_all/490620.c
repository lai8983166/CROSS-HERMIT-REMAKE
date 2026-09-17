
void FUN__text__00490620(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [16];
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(short *)(param_2 + 0xc) = *(short *)(param_2 + 0xc) + 1;
  if (0xb3 < *(short *)(param_2 + 0xc)) {
    *(undefined2 *)(param_2 + 0xc) = 0;
  }
  return;
}

