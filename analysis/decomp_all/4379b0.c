
void __fastcall FUN_004379b0(int param_1)

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
  if (*(int *)(param_1 + 8) != 0) {
    local_c = *(undefined4 *)(param_1 + 8);
    FUN_00428ad0(local_c);
    *(undefined4 *)(local_8 + 8) = 0;
  }
  if (*(int *)(local_8 + 0xc) != 0) {
    local_10 = *(undefined4 *)(local_8 + 0xc);
    FUN_00428ad0(local_10);
    *(undefined4 *)(local_8 + 0xc) = 0;
  }
  local_8 = 0x437a2c;
  __chkesp();
  return;
}

