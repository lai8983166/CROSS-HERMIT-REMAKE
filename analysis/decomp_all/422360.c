
void __thiscall FUN__text__00422360(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [11];
  undefined4 uStack_20;
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(int *)(param_1 + 8);
  *(undefined4 *)(param_1 + 0x14) = param_2;
  local_8 = param_1;
  FUN__text__00422560(0x10000);
  (*API_NTDLL_DLL_RtlEnterCriticalSection)(local_c + 0x100);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_ResetEvent)(*(undefined4 *)(local_8 + 0x1c));
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_SetEvent)(*(undefined4 *)(local_c + 0x118));
  FUN__text__0056ce80();
  (*API_NTDLL_DLL_RtlLeaveCriticalSection)(local_c + 0x100);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_WaitForSingleObject)(*(undefined4 *)(local_8 + 0x1c),0xffffffff);
  FUN__text__0056ce80();
  FUN__text__004225a0(0x10000);
  uStack_20 = 0x42242e;
  FUN__text__0056ce80();
  return;
}

