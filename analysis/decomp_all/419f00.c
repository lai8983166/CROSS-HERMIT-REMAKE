
void __fastcall FUN_00419f00(int param_1)

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
  if (*(int *)(param_1 + 0x177c) != 0) {
    local_c = *(undefined4 *)(param_1 + 0x177c);
    local_8 = param_1;
    FUN_00428ad0(local_c);
    *(undefined4 *)(local_8 + 0x177c) = 0;
  }
  local_8 = 0x419f5b;
  __chkesp();
  return;
}

