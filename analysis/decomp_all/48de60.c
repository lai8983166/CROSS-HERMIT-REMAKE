
void FUN__text__0048de60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = *(int *)(param_1 + 0x518);
  while (iVar1 != 0) {
    local_c = *(undefined4 *)(param_1 + 0x518);
    FUN__text__00427a80(local_c);
    FUN__text__00427e70(local_c);
    iVar1 = *(int *)(param_1 + 0x518);
  }
  local_8 = 0x48ded5;
  FUN__text__0056ce80();
  return;
}

