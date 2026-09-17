
void __fastcall FUN_004181b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    local_10 = (int *)(local_8 + 0x17c + local_c * 0x14);
    if (*local_10 != 0) {
      local_14 = *local_10;
      FUN_00428ad0(local_14);
      *local_10 = 0;
    }
  }
  _memset((void *)(local_8 + 0x174),0,0xd0);
  local_8 = 0x418244;
  __chkesp();
  return;
}

