
void FUN__text__0048e0a0(int param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  byte *local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0x518) != 0) {
    local_c = *(int *)(param_1 + 0x518);
    do {
      local_14 = *(byte **)(local_c + 8);
      if (*local_14 == param_2) {
        local_10 = *(undefined4 *)(local_c + 4);
        FUN__text__00427a80(local_c);
        break;
      }
      local_c = *(int *)(local_c + 4);
    } while (local_c != 0);
  }
  local_8 = 0x48e133;
  FUN__text__0056ce80();
  return;
}

