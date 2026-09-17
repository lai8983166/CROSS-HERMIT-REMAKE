
void __fastcall FUN_00425450(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 8) != 0) {
    local_10 = *(int *)(param_1 + 8);
    local_c = local_10;
    local_8 = param_1;
    if (local_10 == 0) {
      local_14 = 0;
    }
    else {
      local_14 = FUN_00425380(3);
    }
    *(undefined4 *)(local_8 + 8) = 0;
  }
  local_8 = 0x4254b8;
  __chkesp();
  return;
}

