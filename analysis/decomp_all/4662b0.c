
void FUN_004662b0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN_004665c0();
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    FUN_0040ac90(local_8 + 0x109388 + local_c * 0x520);
  }
  for (local_c = 0; local_c != 2; local_c = local_c + 1) {
    if (*(int *)(local_8 + 0x2a6e8 + local_c * 4) != 0) {
      FUN_00464d30();
      local_14 = *(int *)(local_8 + 0x2a6e8 + local_c * 4);
      local_10 = local_14;
      if (local_14 == 0) {
        local_18 = 0;
      }
      else {
        local_18 = FUN_004663b0(1);
      }
      *(undefined4 *)(local_8 + 0x2a6e8 + local_c * 4) = 0;
    }
  }
  local_8 = 0x4663a9;
  __chkesp();
  return;
}

