
void __fastcall FUN_0043cf10(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x98) != 0) {
    local_c = *(undefined4 *)(param_1 + 0x98);
    FUN_00428ad0(local_c);
    *(undefined4 *)(local_8 + 0x98) = 0;
  }
  if (*(int *)(local_8 + 0x9c) != 0) {
    local_10 = *(undefined4 *)(local_8 + 0x9c);
    FUN_00428ad0(local_10);
    *(undefined4 *)(local_8 + 0x9c) = 0;
  }
  if (*(int *)(local_8 + 0xa0) != 0) {
    local_14 = *(undefined4 *)(local_8 + 0xa0);
    FUN_00428ad0(local_14);
    *(undefined4 *)(local_8 + 0xa0) = 0;
  }
  local_8 = 0x43cfcd;
  __chkesp();
  return;
}

