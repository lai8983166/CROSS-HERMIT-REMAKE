
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_005840d0(int param_1)

{
  bool bVar1;
  int iVar2;
  code *local_20;
  undefined4 *local_1c;
  undefined4 local_18;
  int local_14;
  undefined4 local_c;
  int local_8;
  
  bVar1 = false;
  switch(param_1) {
  case 2:
    local_1c = &DAT_0080a68c;
    local_20 = DAT_0080a68c;
    bVar1 = true;
    break;
  default:
    return 0xffffffff;
  case 4:
  case 8:
  case 0xb:
    local_8 = FUN_005753b0();
    iVar2 = FUN_00584310(param_1,*(undefined4 *)(local_8 + 0x50));
    local_1c = (undefined4 *)(iVar2 + 8);
    local_20 = (code *)*local_1c;
    break;
  case 0xf:
    local_1c = &DAT_0080a698;
    local_20 = DAT_0080a698;
    bVar1 = true;
    break;
  case 0x15:
    local_1c = &DAT_0080a690;
    local_20 = DAT_0080a690;
    bVar1 = true;
    break;
  case 0x16:
    local_1c = &DAT_0080a694;
    local_20 = DAT_0080a694;
    bVar1 = true;
  }
  if (bVar1) {
    FUN_00577040(1);
  }
  if (local_20 != (code *)0x1) {
    if (local_20 == (code *)0x0) {
      if (bVar1) {
        FUN_005770e0(1);
      }
                    /* WARNING: Subroutine does not return */
      __exit(3);
    }
    if (((param_1 == 8) || (param_1 == 0xb)) || (param_1 == 4)) {
      local_18 = *(undefined4 *)(local_8 + 0x54);
      *(undefined4 *)(local_8 + 0x54) = 0;
      if (param_1 == 8) {
        local_c = *(undefined4 *)(local_8 + 0x58);
        *(undefined4 *)(local_8 + 0x58) = 0x8c;
      }
    }
    if (param_1 == 8) {
      for (local_14 = DAT_00761de0; local_14 < DAT_00761de0 + _DAT_00761de4; local_14 = local_14 + 1
          ) {
        *(undefined4 *)(*(int *)(local_8 + 0x50) + 8 + local_14 * 0xc) = 0;
      }
    }
    else {
      *local_1c = 0;
    }
    if (bVar1) {
      FUN_005770e0(1);
    }
    if (param_1 == 8) {
      (*local_20)(8,*(undefined4 *)(local_8 + 0x58));
    }
    else {
      (*local_20)(param_1);
      if ((param_1 != 0xb) && (param_1 != 4)) {
        return 0;
      }
    }
    *(undefined4 *)(local_8 + 0x54) = local_18;
    if (param_1 == 8) {
      *(undefined4 *)(local_8 + 0x58) = local_c;
    }
    return 0;
  }
  if (bVar1) {
    FUN_005770e0(1);
  }
  return 0;
}

