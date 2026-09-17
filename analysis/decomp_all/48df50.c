
void __thiscall FUN__text__0048df50(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_2 + 0x518) != 0) {
    local_c = *(int *)(param_2 + 0x518);
    local_8 = param_1;
    do {
      local_14 = *(undefined4 *)(local_c + 8);
      iVar1 = FUN__text__0048e1b0(local_14);
      if ((iVar1 == 0) && (iVar1 = FUN__text__0048e140(local_14), iVar1 != 0)) {
        local_c = *(int *)(local_c + 4);
      }
      else {
        local_10 = *(int *)(local_c + 4);
        FUN__text__00427a80(local_c);
        FUN__text__00427cd0(local_c);
        local_c = local_10;
      }
    } while (local_c != 0);
  }
  local_8 = 0x48e00b;
  FUN__text__0056ce80();
  return;
}

