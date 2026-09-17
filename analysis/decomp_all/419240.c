
void __fastcall FUN_00419240(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*param_1 != 0) && ((char)param_1[0x5dc] != '\0')) {
    local_8 = param_1;
    (**(code **)(*(int *)*param_1 + 0x10))(*param_1);
    local_c = __chkesp();
    if (local_c == 0) {
      local_8[0x5db] = -1;
      *(undefined1 *)(local_8 + 0x5dc) = 0;
    }
  }
  local_8 = (int *)0x4192d0;
  __chkesp();
  return;
}

