
void __thiscall
FUN__text__004388e0(int param_1,short param_2,short param_3,short param_4,short param_5,int param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_18 = (int)param_4 - (int)param_2;
  local_1c = (int)param_5 - (int)param_3;
  if (local_18 < 0) {
    local_24 = -1;
    local_18 = -local_18;
  }
  else {
    local_24 = 1;
  }
  if (local_1c < 0) {
    local_28 = -1;
    local_1c = -local_1c;
  }
  else {
    local_28 = 1;
  }
  local_c = (int)param_2;
  local_10 = (int)param_3;
  local_20 = 0;
  local_8 = param_1;
  if (local_18 < local_1c) {
    for (local_14 = 0; local_14 < local_1c; local_14 = local_14 + 1) {
      local_10 = local_10 + local_28;
      local_20 = local_20 + local_18;
      if (local_1c <= local_20) {
        local_c = local_c + local_24;
        local_20 = local_20 - local_1c;
      }
      iVar1 = FUN__text__0043bfa0(local_c,local_10,*(undefined4 *)(local_8 + 0x14));
      if ((iVar1 == 0) ||
         ((param_6 != 0 && (iVar1 = FUN__text__0043c0c0(local_c,local_10), iVar1 != 0)))) break;
    }
  }
  else {
    for (local_14 = 0; local_14 < local_18; local_14 = local_14 + 1) {
      local_c = local_c + local_24;
      local_20 = local_20 + local_1c;
      if (local_18 <= local_20) {
        local_10 = local_10 + local_28;
        local_20 = local_20 - local_18;
      }
      iVar1 = FUN__text__0043bfa0(local_c,local_10,*(undefined4 *)(local_8 + 0x14));
      if ((iVar1 == 0) ||
         ((param_6 != 0 && (iVar1 = FUN__text__0043c0c0(local_c,local_10), iVar1 != 0)))) break;
    }
  }
  local_8 = 0x438abf;
  FUN__text__0056ce80();
  return;
}

