
void FUN_004258c0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN_00425c10();
  if (*(int *)(local_8 + 4) != 0) {
    local_c = FUN_0056cd2c(*(undefined4 *)(local_8 + 4),*(undefined4 *)(local_8 + 8));
    *(undefined4 *)(local_8 + 8) = 0;
    *(undefined4 *)(local_8 + 4) = 0;
  }
  local_8 = 0x425927;
  __chkesp();
  return;
}

