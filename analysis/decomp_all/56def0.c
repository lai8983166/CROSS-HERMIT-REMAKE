
void FUN_0056def0(undefined4 param_1,undefined4 param_2,int param_3,code *param_4)

{
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  puStack_c = &DAT_005f94c8;
  puStack_10 = &DAT_00576b9c;
  local_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_14;
  local_8 = 0;
  while (param_3 = param_3 + -1, -1 < param_3) {
    (*param_4)();
  }
  *unaff_FS_OFFSET = local_14;
  return;
}

