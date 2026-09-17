
void FUN_00421d50(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int *local_18;
  int *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN_00421e20(param_1);
  if (local_c == -1) {
    FUN_0042b2d0("ERROR: no delete task link = %08x\n",param_1);
    iVar2 = FUN_00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                         DAT_005ff600 + 9,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    local_14 = (int *)(local_8 + local_c * 8);
    local_10 = *local_14;
    while (*local_14 != param_1) {
      local_10 = *local_14;
      local_14 = (int *)(local_10 + 0xc);
    }
    local_18 = (int *)(param_1 + 0xc);
    *local_14 = *local_18;
  }
  local_8 = 0x421e1a;
  __chkesp();
  return;
}

