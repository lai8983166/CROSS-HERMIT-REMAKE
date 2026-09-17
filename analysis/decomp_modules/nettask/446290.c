
void FUN__text__00446290(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != *param_1; local_c = local_c + 1) {
    FUN__text__00407780();
  }
  if (param_1[1] != 0) {
    local_14 = param_1[1];
    local_10 = local_14;
    if (local_14 == 0) {
      local_18 = 0;
    }
    else {
      local_18 = FUN__text__004461f0(3);
    }
    param_1[1] = 0;
  }
  *param_1 = 0;
  local_8 = 0x446334;
  FUN__text__0056ce80();
  return;
}

