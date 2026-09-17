
void __fastcall FUN_0040d8c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x10) != 0) {
    local_c = *(undefined4 *)(param_1 + 0x10);
    FUN_00428ad0(local_c);
    *(undefined4 *)(local_8 + 0x10) = 0;
  }
  if (*(int *)(local_8 + 0x14) != 0) {
    local_10 = *(undefined4 *)(local_8 + 0x14);
    FUN_00428ad0(local_10);
    *(undefined4 *)(local_8 + 0x14) = 0;
  }
  if (*(int *)(local_8 + 0x24) != 0) {
    (**(code **)(**(int **)(local_8 + 0x24) + 8))(*(undefined4 *)(local_8 + 0x24));
    __chkesp();
    *(undefined4 *)(local_8 + 0x24) = 0;
  }
  local_8 = 0x40d96a;
  __chkesp();
  return;
}

