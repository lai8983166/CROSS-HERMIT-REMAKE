
void __thiscall FUN__text__004942b0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int *local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = (int *)(param_1 + 0xddc88);
  *local_18 = 0;
  local_c = param_1 + 0x116098 + param_2 * 0x2c;
  local_8 = param_1;
  FUN__text__00427b70(local_c + 0x10);
  while (local_10 = FUN__text__00427bf0(), local_10 != 0) {
    local_14 = *(int *)(local_10 + 8);
    if ((local_14 == 0) &&
       (iVar2 = FUN__text__00424f80("wk!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlKeySelect.cpp",
                                    DAT_0061929c + 0x10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_18[*local_18 + 1] = local_14;
    *local_18 = *local_18 + 1;
  }
  local_10 = 0;
  if (*local_18 != 0) {
    local_20 = -1;
    for (local_1c = 0; local_1c != *local_18; local_1c = local_1c + 1) {
      iVar2 = FUN__text__00469480(local_18[local_1c + 1]);
      if (iVar2 != 0) {
        local_20 = local_1c;
        break;
      }
    }
    if ((local_20 != -1) && (*(char *)(local_18[local_20 + 1] + 0x28c) != '\0')) {
      FUN__text__0043b400(*(int *)(local_18[local_20 + 1] + 0x2ec) >> 0x10,
                          *(int *)(local_18[local_20 + 1] + 0x2f0) >> 0x10);
    }
    for (local_1c = 0; local_1c != *(int *)(local_8 + 0x108b50); local_1c = local_1c + 1) {
      *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_1c * 4) + 0x28c) = 0;
    }
    for (local_1c = 0; local_1c != *local_18; local_1c = local_1c + 1) {
      *(undefined1 *)(local_18[local_1c + 1] + 0x28c) = 1;
    }
    FUN__text__0046f170();
  }
  local_8 = 0x494499;
  FUN__text__0056ce80();
  return;
}

