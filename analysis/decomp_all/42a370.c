
void FUN__text__0042a370(undefined4 param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_70 [16];
  int *local_30;
  int local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined *local_20;
  undefined4 local_1c;
  undefined4 local_18;
  code *local_14;
  int local_10;
  undefined4 local_c;
  undefined *local_8;
  
  puVar2 = local_70;
  for (iVar1 = 0x1b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = (undefined *)0x0;
  local_30 = (int *)0x0;
  local_2c = 0;
  (*API_SHELL32_DLL_SHGetMalloc)(&local_30);
  iVar1 = FUN__text__0056ce80();
  if (iVar1 == 0) {
    local_28 = param_1;
    local_24 = 0;
    local_20 = &DAT_007a2420;
    local_1c = param_2;
    local_18 = 1;
    if (param_3 == 0) {
      local_14 = (code *)0x0;
      local_10 = 0;
    }
    else {
      local_14 = FUN__text__0042a4b0;
      local_10 = param_3;
    }
    local_c = 0;
    (*API_SHELL32_DLL_SHBrowseForFolderA)(&local_28);
    local_2c = FUN__text__0056ce80();
    if (local_2c != 0) {
      (*API_SHELL32_DLL_SHGetPathFromIDListA)(local_2c,&DAT_007a2420);
      iVar1 = FUN__text__0056ce80();
      if (iVar1 != 0) {
        local_8 = &DAT_007a2420;
      }
    }
    if (local_2c != 0) {
      (**(code **)(*local_30 + 0x14))(local_30,local_2c);
      FUN__text__0056ce80();
    }
    if (local_30 != (int *)0x0) {
      (**(code **)(*local_30 + 8))(local_30);
      FUN__text__0056ce80();
    }
    FUN__text__004297a0(&DAT_007a2420);
  }
  local_c = 0x42a4a8;
  FUN__text__0056ce80();
  return;
}

