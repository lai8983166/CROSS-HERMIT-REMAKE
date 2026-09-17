
void FUN_0044e330(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_54 [17];
  undefined4 local_10;
  undefined *puStack_c;
  uint local_8;
  
  puStack_c = &DAT_0058f555;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 1;
  FUN_0044e3b0();
  local_8 = local_8 & 0xffffff00;
  FUN_00439410();
  local_8 = 0xffffffff;
  FUN_004209c0();
  *unaff_FS_OFFSET = local_10;
  local_8 = 0x44e3a6;
  __chkesp();
  return;
}

