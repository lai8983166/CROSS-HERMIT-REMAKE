
void __fastcall FUN_00504e10(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_54 [15];
  undefined4 uStack_18;
  undefined4 *local_14;
  undefined4 local_10;
  undefined *puStack_c;
  int local_8;
  
  puStack_c = &DAT_00590af0;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = &PTR_DAT_005ca9d0;
  local_8 = 2;
  local_14 = param_1;
  FUN_0041d280();
  FUN_0040d610();
  local_8._0_1_ = 1;
  FUN_0056de40(local_14 + 0x98,0x54,10,FUN_00464cc0);
  local_8 = (uint)local_8._1_3_ << 8;
  FUN_00407710();
  local_8 = 0xffffffff;
  FUN_00439f80();
  *unaff_FS_OFFSET = local_10;
  uStack_18 = 0x504ec8;
  __chkesp();
  return;
}

