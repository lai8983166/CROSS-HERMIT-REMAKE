
void __fastcall FUN_00439dd0(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 == 1) {
    local_8 = param_1;
    (*API_NTDLL_DLL_RtlDeleteCriticalSection)(param_1 + 1);
    __chkesp();
    *local_8 = 0;
  }
  local_8 = (int *)0x439e23;
  __chkesp();
  return;
}

