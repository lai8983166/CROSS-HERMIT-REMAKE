
void __thiscall FUN_00417950(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  undefined4 local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int *)(param_1 + param_2 * 8);
  local_10 = *local_c;
  if (local_c[1] != 0) {
    if (local_10 != 0) {
      for (local_14 = 0; local_14 != local_c[1]; local_14 = local_14 + 1) {
        *(undefined4 *)(local_10 + local_14 * 0x10) = 0;
      }
      local_1c = local_10;
      local_18 = local_10;
      if (local_10 == 0) {
        local_20 = 0;
      }
      else {
        local_8 = param_1;
        local_20 = FUN_00417850(3);
      }
    }
    *local_c = 0;
    local_c[1] = 0;
  }
  local_8 = 0x417a09;
  __chkesp();
  return;
}

