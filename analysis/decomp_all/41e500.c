
void __fastcall FUN_0041e500(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)(param_1 + 0x22) = 0;
  *(undefined1 *)(param_1 + 0x21) = 0;
  local_8 = param_1;
  iVar1 = FUN_0041d790();
  if (iVar1 != 0) {
    (**(code **)(**(int **)(local_8 + 4) + 0x24))(*(undefined4 *)(local_8 + 4));
    local_c = __chkesp();
    if (local_c < 0) {
      FUN_0041d040(local_c);
    }
  }
  local_8 = 0x41e584;
  __chkesp();
  return;
}

