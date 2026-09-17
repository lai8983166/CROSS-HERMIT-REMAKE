
void FUN__text__0046b0f0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 == 1) {
    *(undefined1 *)(param_1 + 7) = 1;
  }
  else {
    *(undefined1 *)(param_1 + 7) = 0;
  }
  return;
}

