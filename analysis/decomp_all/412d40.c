
void FUN__text__00412d40(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = *param_1;
    FUN__text__0041d280();
    FUN__text__0040d610();
    local_10 = *param_1;
    local_c = local_10;
    if (local_10 == 0) {
      local_14 = 0;
    }
    else {
      local_14 = FUN__text__00412dd0(1);
    }
    *param_1 = 0;
  }
  local_8 = 0x412dc6;
  FUN__text__0056ce80();
  return;
}

