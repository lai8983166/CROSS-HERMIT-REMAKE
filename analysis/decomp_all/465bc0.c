
void FUN_00465bc0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  undefined *puStack_c;
  int local_8;
  
  puStack_c = &DAT_00590080;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_64;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 0x14;
  FUN_00465e60();
  local_8._0_1_ = 0x13;
  FUN_0056de40(local_14 + 0x116098,0x2c,10,&DAT_00465b80);
  local_8._0_1_ = 0x12;
  FUN_0056de40(local_14 + 0x108930,0x80,4,FUN_00407710);
  local_8._0_1_ = 0x11;
  FUN_0056de40(local_14 + 0x100930,0x80,0x100,FUN_00407710);
  local_8._0_1_ = 0x10;
  FUN_0056de40(local_14 + 0xf0930,0x80,0x200,FUN_00407710);
  local_8._0_1_ = 0xf;
  FUN_0056de40(local_14 + 0xe0930,0x80,0x200,FUN_00407710);
  local_8._0_1_ = 0xe;
  FUN_0056de40(local_14 + 0xde930,0x80,0x40,FUN_00407710);
  local_8._0_1_ = 0xd;
  FUN_0056de40(local_14 + 0xde7b0,0x80,3,FUN_00407710);
  local_8._0_1_ = 0xc;
  FUN_00407710();
  local_8._0_1_ = 0xb;
  FUN_00407710();
  local_8._0_1_ = 10;
  FUN_00407710();
  local_8._0_1_ = 9;
  FUN_00407710();
  local_8._0_1_ = 8;
  FUN_00407710();
  local_8._0_1_ = 7;
  FUN_00407710();
  local_8._0_1_ = 6;
  FUN_0056de40(local_14 + 0xde460,0x28,2,FUN_004275b0);
  local_8._0_1_ = 5;
  FUN_0056de40(local_14 + 0xdb86c,0x88,0x14,&DAT_00465b00);
  local_8._0_1_ = 4;
  FUN_0040bb20();
  local_8._0_1_ = 3;
  if (local_14 == 0) {
    local_18 = 0;
  }
  else {
    local_18 = local_14 + 0x2a634;
  }
  FUN_00437940();
  local_8._0_1_ = 2;
  if (local_14 == 0) {
    local_1c = 0;
  }
  else {
    local_1c = local_14 + 0x2a55c;
  }
  FUN_0044e330();
  local_8._0_1_ = 1;
  if (local_14 == 0) {
    local_20 = 0;
  }
  else {
    local_20 = local_14 + 0x3d68;
  }
  FUN_0043a270();
  local_8 = (uint)local_8._1_3_ << 8;
  if (local_14 == 0) {
    local_24 = 0;
  }
  else {
    local_24 = local_14 + 0x1798;
  }
  FUN_00464800();
  local_8 = 0xffffffff;
  FUN_00464ac0();
  *unaff_FS_OFFSET = local_10;
  __chkesp();
  return;
}

