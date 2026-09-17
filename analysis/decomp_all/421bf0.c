
void __fastcall FUN_00421bf0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 0x20; local_c = local_c + 1) {
    while (local_14 = (int *)(local_8 + local_c * 8), *local_14 != 0) {
      local_10 = *local_14;
      FUN_00422090(local_10);
    }
  }
  local_8 = 0x421c60;
  __chkesp();
  return;
}

