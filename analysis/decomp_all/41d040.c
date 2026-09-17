
void FUN_0041d040(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_148 [16];
  undefined1 local_108 [244];
  undefined4 uStack_14;
  
  puVar2 = local_148;
  for (iVar1 = 0x51; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN_0056d810(local_108,"DxShowErr : %08x : ");
  FUN_0042b2d0(&DAT_00592a18,local_108);
  (*API_QUARTZ_DLL_AMGetErrorTextA)(param_1,local_108,0x104);
  __chkesp();
  FUN_0042b2d0(&DAT_00592f50,local_108);
  uStack_14 = 0x41d0c9;
  __chkesp();
  return;
}

