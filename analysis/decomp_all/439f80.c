
void __fastcall FUN_00439f80(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  undefined4 local_58 [16];
  undefined4 *local_18;
  undefined4 *local_14;
  undefined4 local_10;
  undefined *puStack_c;
  uint local_8;
  
  puStack_c = &DAT_0058f131;
  local_10 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &local_10;
  puVar2 = local_58;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = &PTR_DAT_00595560;
  local_8 = 1;
  local_14 = param_1;
  FUN_0042b2d0(&DAT_00595568,param_1);
  local_8 = local_8 & 0xffffff00;
  if (local_14 == (undefined4 *)0x0) {
    local_18 = (undefined4 *)0x0;
  }
  else {
    local_18 = local_14 + 0xb;
  }
  FUN_004209c0();
  local_8 = 0xffffffff;
  FUN_004222d0();
  *unaff_FS_OFFSET = local_10;
  local_8 = 0x43a01d;
  __chkesp();
  return;
}

