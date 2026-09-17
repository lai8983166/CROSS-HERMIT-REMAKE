
void FUN_0043a320(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN_0043cf10();
  if (local_8[0x98ee] != 0) {
    local_c = local_8[0x98ee];
    FUN_00428ad0(local_c);
    local_8[0x98ee] = 0;
  }
  if (local_8[0x98ef] != 0) {
    local_10 = local_8[0x98ef];
    FUN_00428ad0(local_10);
    local_8[0x98ef] = 0;
  }
  if (local_8[0x98ed] != -1) {
    FUN_0041f4e0(local_8[0x98ed]);
    local_8[0x98ed] = -1;
  }
  FUN_00407780();
  FUN_00407780();
  FUN_00407780();
  if (local_8[0x9963] != 0) {
    local_14 = local_8[0x9963];
    FUN_00428ad0(local_14);
    local_8[0x9963] = 0;
  }
  if (local_8[0x9968] != 0) {
    if (*(int *)local_8[0x9968] != 0) {
      local_18 = *(undefined4 *)local_8[0x9968];
      FUN_00428ad0(local_18);
      *(undefined4 *)local_8[0x9968] = 0;
    }
    local_1c = local_8[0x9968];
    FUN_00428ad0(local_1c);
    local_8[0x9968] = 0;
  }
  if (local_8[0x9967] != 0) {
    local_20 = local_8[0x9967];
    FUN_00428ad0(local_20);
    local_8[0x9967] = 0;
  }
  if (*local_8 != 0) {
    local_24 = *local_8;
    FUN_00428ad0(local_24);
    *local_8 = 0;
  }
  local_8 = (int *)0x43a503;
  __chkesp();
  return;
}

