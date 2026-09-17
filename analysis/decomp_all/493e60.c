
void __fastcall FUN_00493e60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined1 *local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 != 10; local_10 = local_10 + 1) {
    local_c = (undefined1 *)(local_8 + 0x116098 + local_10 * 0x2c);
    *local_c = 0;
    FUN_004275f0();
  }
  local_8 = 0x493ec8;
  __chkesp();
  return;
}

