
void __thiscall FUN_00577040(undefined4 param_1,int param_2)

{
  int iVar1;
  
  if (*(int *)(&DAT_00761df0 + param_2 * 4) == 0) {
    iVar1 = __malloc_dbg(0x18,2,"mlock.c",0xe1,param_1);
    if (iVar1 == 0) {
      __amsg_exit(0x11);
    }
    FUN_00577040(0x11);
    if (*(int *)(&DAT_00761df0 + param_2 * 4) == 0) {
      (*API_NTDLL_DLL_RtlInitializeCriticalSection)(iVar1);
      *(int *)(&DAT_00761df0 + param_2 * 4) = iVar1;
    }
    else {
      __free_dbg(iVar1,2);
    }
    FUN_005770e0(0x11);
  }
  (*API_NTDLL_DLL_RtlEnterCriticalSection)(*(undefined4 *)(&DAT_00761df0 + param_2 * 4));
  return;
}

