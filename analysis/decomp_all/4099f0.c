
void FUN_004099f0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_54 [17];
  undefined4 local_10;
  undefined *puStack_c;
  uint local_8;
  
  puStack_c = &DAT_0058ebd5;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 1;
  FUN_00409a70();
  local_8 = local_8 & 0xffffff00;
  FUN_0041eb30();
  local_8 = 0xffffffff;
  FUN_004209c0();
  *unaff_FS_OFFSET = local_10;
  local_8 = 0x409a66;
  __chkesp();
  return;
}

