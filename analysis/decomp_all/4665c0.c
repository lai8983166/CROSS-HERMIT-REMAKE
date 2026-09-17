
void __fastcall FUN_004665c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = param_1 + 0x10c680;
  local_8 = param_1;
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    local_10 = local_8 + 0x10c680 + local_c * 0x520;
    FUN_0040ac90(local_10 + 0x48);
  }
  local_8 = 0x466637;
  __chkesp();
  return;
}

