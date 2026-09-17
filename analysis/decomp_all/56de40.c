
void FUN_0056de40(undefined4 param_1,undefined4 param_2,int param_3,code *param_4)

{
  undefined4 unaff_EBX;
  undefined4 unaff_ESI;
  undefined4 *unaff_FS_OFFSET;
  undefined4 uVar1;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  puStack_c = &DAT_005f94b8;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  local_8 = 0;
  while( true ) {
    param_3 = param_3 + -1;
    if (param_3 < 0) break;
    (*param_4)();
  }
  uVar1 = 1;
  local_8 = 0xffffffff;
  FUN_0056deb5();
  FUN_0056ded1(unaff_ESI,unaff_EBX,uVar1);
  return;
}

