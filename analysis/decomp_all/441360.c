
void FUN_00441360(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_54 [15];
  undefined4 uStack_18;
  int local_14;
  undefined4 local_10;
  undefined *puStack_c;
  uint local_8;
  
  puStack_c = &DAT_0058f227;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 1;
  FUN_004413f0();
  local_8 = local_8 & 0xffffff00;
  FUN_0056de40(local_14 + 0x84,0x8c,0x14,FUN_00409360);
  local_8 = 0xffffffff;
  FUN_00407710();
  *unaff_FS_OFFSET = local_10;
  uStack_18 = 0x4413e8;
  __chkesp();
  return;
}

