
void FUN_004036c0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_54 [17];
  undefined4 local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  puStack_c = &DAT_0058eae9;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 0;
  FUN_00403730();
  local_8 = 0xffffffff;
  FUN_0041f9e0();
  *unaff_FS_OFFSET = local_10;
  local_8 = 0x403727;
  __chkesp();
  return;
}

