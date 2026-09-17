
void __fastcall FUN_00466f00(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined4 local_1c;
  int local_18;
  int local_14;
  int local_10;
  char *local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 != 0x200; local_10 = local_10 + 1) {
    local_c = (char *)(local_8 + 0x2a6f0 + local_10 * 8);
    if (*local_c != '\0') {
      FUN_00464d30();
      local_18 = *(int *)(local_c + 4);
      local_14 = local_18;
      if (local_18 == 0) {
        local_1c = 0;
      }
      else {
        local_1c = FUN_004663b0(1);
      }
      local_c[4] = '\0';
      local_c[5] = '\0';
      local_c[6] = '\0';
      local_c[7] = '\0';
      _memset(local_c,0,8);
    }
  }
  local_8 = 0x466fb3;
  __chkesp();
  return;
}

