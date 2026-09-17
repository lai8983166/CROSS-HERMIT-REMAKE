
void FUN_00439410(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_54 [17];
  undefined4 local_10;
  undefined *puStack_c;
  int local_8;
  
  puStack_c = &DAT_0058f0d1;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 2;
  FUN_004394a0();
  local_8._0_1_ = 1;
  FUN_004275b0();
  local_8 = (uint)local_8._1_3_ << 8;
  FUN_004275b0();
  local_8 = 0xffffffff;
  FUN_004275b0();
  *unaff_FS_OFFSET = local_10;
  local_8 = 0x439495;
  __chkesp();
  return;
}

