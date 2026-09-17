
void FUN__text__00493020(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0x510) == 0) {
    *(undefined4 *)(param_2 + 4) = 0;
    *(int *)(param_1 + 0x510) = param_2;
  }
  else {
    *(undefined4 *)(param_2 + 4) = *(undefined4 *)(param_1 + 0x510);
    *(int *)(param_1 + 0x510) = param_2;
  }
  return;
}

