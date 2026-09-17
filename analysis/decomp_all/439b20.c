
void FUN__text__00439b20(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 4) == 0) {
    FUN__text__00427990(param_1,param_2);
  }
  else {
    local_18 = *(int *)(param_2 + 8);
    local_1c = *(int *)(local_18 + 0x10);
    local_c = *(int *)(param_1 + 4);
    local_10 = param_1;
    while ((local_c != 0 && (local_14 = *(int *)(local_c + 8), *(int *)(local_14 + 0x10) < local_1c)
           )) {
      local_10 = local_c;
      local_c = *(int *)(local_c + 4);
    }
    local_c = local_10;
    FUN__text__00427990(local_10,param_2);
  }
  local_8 = 0x439bd9;
  FUN__text__0056ce80();
  return;
}

