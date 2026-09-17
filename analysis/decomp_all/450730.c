
void FUN__text__00450730(int *param_1)

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
  if (*param_1 != 0) {
    local_c = *param_1;
    FUN__text__0040d610();
    FUN__text__0041d280();
    local_14 = *param_1;
    local_10 = local_14;
    if (local_14 == 0) {
      local_18 = 0;
    }
    else {
      local_18 = FUN__text__00412dd0(1);
    }
    *param_1 = 0;
  }
  local_8 = 0x4507bb;
  FUN__text__0056ce80();
  return;
}

