
void FUN_00417cc0(void)

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
  FUN_00419240();
  FUN_00419de0();
  FUN_00419f00();
  FUN_0041a6d0();
  FUN_00419540();
  FUN_00419710();
  FUN_004198b0();
  FUN_00418b20();
  FUN_004181b0();
  if (local_8[0x5b] != 0) {
    local_c = local_8[0x5b];
    FUN_00428ad0(local_c);
    local_8[0x5b] = 0;
  }
  FUN_00418720();
  if ((char)local_8[0x5c] != '\0') {
    (*API_NTDLL_DLL_RtlDeleteCriticalSection)(local_8 + 0x51);
    __chkesp();
    *(undefined1 *)(local_8 + 0x5c) = 0;
  }
  if (local_8[1] != 0) {
    (**(code **)(*(int *)local_8[1] + 8))(local_8[1]);
    __chkesp();
    local_8[1] = 0;
  }
  if (*local_8 != 0) {
    (**(code **)(*(int *)*local_8 + 8))(*local_8);
    __chkesp();
    *local_8 = 0;
  }
  local_8 = (int *)0x417df6;
  __chkesp();
  return;
}

