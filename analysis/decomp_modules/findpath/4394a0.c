
void FUN_004394a0(void)

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
  FUN_004275f0();
  FUN_004275f0();
  if (*(int *)(local_8 + 0x88) != 0) {
    local_c = *(undefined4 *)(local_8 + 0x88);
    FUN_00428ad0(local_c);
    *(undefined4 *)(local_8 + 0x88) = 0;
  }
  local_8 = 0x439513;
  __chkesp();
  return;
}

