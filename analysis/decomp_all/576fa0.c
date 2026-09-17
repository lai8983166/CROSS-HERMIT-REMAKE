
void FUN__text__00576fa0(void)

{
  int local_8;
  
  for (local_8 = 0; local_8 < 0x30; local_8 = local_8 + 1) {
    if ((((*(int *)(&DAT_00761df0 + local_8 * 4) != 0) && (local_8 != 0x11)) && (local_8 != 0xd)) &&
       ((local_8 != 9 && (local_8 != 1)))) {
      (*API_NTDLL_DLL_RtlDeleteCriticalSection)(*(undefined4 *)(&DAT_00761df0 + local_8 * 4));
      __free_dbg(*(undefined4 *)(&DAT_00761df0 + local_8 * 4),2);
    }
  }
  (*API_NTDLL_DLL_RtlDeleteCriticalSection)(PTR_DAT_00761e14);
  (*API_NTDLL_DLL_RtlDeleteCriticalSection)(PTR_DAT_00761e24);
  (*API_NTDLL_DLL_RtlDeleteCriticalSection)(PTR_DAT_00761e34);
  (*API_NTDLL_DLL_RtlDeleteCriticalSection)(PTR_DAT_00761df4);
  return;
}

