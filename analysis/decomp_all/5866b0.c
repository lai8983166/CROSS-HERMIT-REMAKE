
void FUN_005866b0(uint param_1)

{
  (*API_NTDLL_DLL_RtlLeaveCriticalSection)
            ((&DAT_0080a800)[(int)param_1 >> 5] + 0xc + (param_1 & 0x1f) * 0x24);
  return;
}

