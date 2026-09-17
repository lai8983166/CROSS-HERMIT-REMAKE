
void FUN_00424f80(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  undefined4 uStack_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (DAT_0079a640 == 0) {
    FUN_0056e2e0(0);
  }
  uStack_c = 0x424fb9;
  __chkesp();
  return;
}

