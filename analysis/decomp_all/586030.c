
int FUN__text__00586030(void)

{
  int iVar1;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = 0;
  FUN__text__00577040(2);
  for (local_c = 3; local_c < DAT_0080bb60; local_c = local_c + 1) {
    if (*(int *)(DAT_0080ab50 + local_c * 4) != 0) {
      if ((*(uint *)(*(int *)(DAT_0080ab50 + local_c * 4) + 0xc) & 0x83) != 0) {
        iVar1 = FUN__text__0056e4a0(*(undefined4 *)(DAT_0080ab50 + local_c * 4));
        if (iVar1 != -1) {
          local_8 = local_8 + 1;
        }
      }
      if (0x13 < local_c) {
        (*API_NTDLL_DLL_RtlDeleteCriticalSection)(*(int *)(DAT_0080ab50 + local_c * 4) + 0x20);
        __free_dbg(*(undefined4 *)(DAT_0080ab50 + local_c * 4),2);
        *(undefined4 *)(DAT_0080ab50 + local_c * 4) = 0;
      }
    }
  }
  FUN__text__005770e0(2);
  return local_8;
}

