
void __thiscall FUN__text__0040cbd0(undefined4 param_1,int *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int *local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (param_2[1] != 0) {
    for (local_c = 0; local_c != *param_2; local_c = local_c + 1) {
      if (*(int *)(param_2[1] + local_c * 4) != 0) {
        local_10 = *(undefined4 *)(param_2[1] + local_c * 4);
        FUN__text__00428ad0(local_10);
        *(undefined4 *)(param_2[1] + local_c * 4) = 0;
      }
    }
  }
  local_14 = param_2;
  FUN__text__00428ad0(param_2);
  local_8 = 0x40cc6f;
  FUN__text__0056ce80();
  return;
}

