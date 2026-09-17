
void FUN_005787e0(int param_1)

{
  undefined4 *unaff_FS_OFFSET;
  undefined4 uStack_2c;
  int iStack_28;
  undefined4 uStack_24;
  int local_20;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fa298;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  if (param_1 != 0) {
    if (DAT_0080ab2c == 3) {
      FUN_00577040(9);
      local_8 = 0;
      local_20 = FUN_00578c00(param_1);
      if (local_20 != 0) {
        FUN_00578cc0(local_20,param_1);
      }
      local_8 = 0xffffffff;
      FUN_0057885b();
      FUN_00578866();
      return;
    }
    if (DAT_0080ab2c == 2) {
      FUN_00577040(9);
      local_8 = 1;
      iStack_28 = FUN_0057ac20(param_1,&uStack_2c,&uStack_24);
      if (iStack_28 != 0) {
        FUN_0057acb0(uStack_2c,uStack_24,iStack_28);
      }
      local_8 = 0xffffffff;
      FUN_005788dd();
      FUN_005788e8();
      return;
    }
    (*API_KERNEL32_DLL_HeapFree)(DAT_0080ab28,0,param_1);
  }
  *unaff_FS_OFFSET = uStack_14;
  return;
}

