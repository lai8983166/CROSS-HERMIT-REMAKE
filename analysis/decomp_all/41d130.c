
void FUN_0041d130(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_54 [15];
  undefined4 uStack_18;
  int local_14;
  undefined4 local_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  puStack_c = &DAT_0058eef9;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_54;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 0;
  FUN_0041d1b0();
  local_8 = 0xffffffff;
  FUN_0056de40(local_14 + 8,0x278,2,&DAT_0041d3c0);
  *unaff_FS_OFFSET = local_10;
  uStack_18 = 0x41d1a7;
  __chkesp();
  return;
}

