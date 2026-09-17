
void FUN_00586620(uint param_1)

{
  int iVar1;
  
  iVar1 = (&DAT_0080a800)[(int)param_1 >> 5] + (param_1 & 0x1f) * 0x24;
  if (*(int *)(iVar1 + 8) == 0) {
    FUN_00577040(0x11);
    if (*(int *)(iVar1 + 8) == 0) {
      (*API_NTDLL_DLL_RtlInitializeCriticalSection)(iVar1 + 0xc);
      *(int *)(iVar1 + 8) = *(int *)(iVar1 + 8) + 1;
    }
    FUN_005770e0(0x11);
  }
  (*API_NTDLL_DLL_RtlEnterCriticalSection)
            ((&DAT_0080a800)[(int)param_1 >> 5] + 0xc + (param_1 & 0x1f) * 0x24);
  return;
}

