
void FUN_0041f480(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != 0x100; local_c = local_c + 1) {
    FUN_0041f4e0(local_c);
  }
  local_8 = 0x41f4d5;
  __chkesp();
  return;
}

