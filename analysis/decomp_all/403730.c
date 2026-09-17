
void __fastcall FUN_00403730(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x2c) != 0) {
    local_10 = FUN_00403a00();
    PTR_DAT_00765720 = PTR_DAT_00765720 + -local_10;
  }
  if (*(int *)(local_8 + 0x2c) != 0) {
    (**(code **)(**(int **)(local_8 + 0x2c) + 8))(*(undefined4 *)(local_8 + 0x2c));
    local_c = __chkesp();
    *(undefined4 *)(local_8 + 0x2c) = 0;
  }
  if (*(int *)(local_8 + 0x30) != 0) {
    (**(code **)(**(int **)(local_8 + 0x30) + 8))(*(undefined4 *)(local_8 + 0x30));
    local_c = __chkesp();
    *(undefined4 *)(local_8 + 0x30) = 0;
  }
  *(undefined4 *)(local_8 + 0x28) = 0;
  local_8 = 0x4037eb;
  __chkesp();
  return;
}

