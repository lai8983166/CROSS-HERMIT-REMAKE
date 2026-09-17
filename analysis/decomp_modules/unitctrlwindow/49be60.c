
void FUN__text__0049be60(int param_1,undefined1 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)(*(int *)(param_1 + 600) + 0x9e) = param_2;
  if (param_3 != 0) {
    *(undefined1 *)(*(int *)(param_1 + 600) + 0x9d) = 1;
  }
  return;
}

