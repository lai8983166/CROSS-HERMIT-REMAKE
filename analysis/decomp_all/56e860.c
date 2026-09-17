
void FUN_0056e860(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                 undefined4 param_5)

{
  undefined4 *unaff_FS_OFFSET;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9598;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  FUN_00577040(9);
  local_8 = 0;
  FUN_0056e920(param_1,param_3,param_4,param_5);
  local_8 = 0xffffffff;
  FUN_0056e8bd();
  FUN_0056e8c8();
  return;
}

