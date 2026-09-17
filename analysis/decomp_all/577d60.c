
undefined4 * FUN__text__00577d60(void)

{
  undefined4 uVar1;
  undefined4 *local_c;
  int local_8;
  
  local_c = (undefined4 *)0x0;
  FUN__text__00577040(2);
  local_8 = 0;
  do {
    if (DAT_0080bb60 <= local_8) {
LAB__text__00577e8e:
      if (local_c != (undefined4 *)0x0) {
        local_c[1] = 0;
        local_c[3] = 0;
        local_c[2] = 0;
        *local_c = 0;
        local_c[7] = 0;
        local_c[4] = 0xffffffff;
      }
      FUN__text__005770e0(2);
      return local_c;
    }
    if (*(int *)(DAT_0080ab50 + local_8 * 4) == 0) {
      uVar1 = __malloc_dbg(0x38,2,"stream.c",0x55);
      *(undefined4 *)(DAT_0080ab50 + local_8 * 4) = uVar1;
      if (*(int *)(DAT_0080ab50 + local_8 * 4) != 0) {
        (*API_NTDLL_DLL_RtlInitializeCriticalSection)(*(int *)(DAT_0080ab50 + local_8 * 4) + 0x20);
        (*API_NTDLL_DLL_RtlEnterCriticalSection)(*(int *)(DAT_0080ab50 + local_8 * 4) + 0x20);
        local_c = *(undefined4 **)(DAT_0080ab50 + local_8 * 4);
      }
      goto LAB__text__00577e8e;
    }
    if ((*(uint *)(*(int *)(DAT_0080ab50 + local_8 * 4) + 0xc) & 0x83) == 0) {
      FUN__text__005772b0(local_8,*(undefined4 *)(DAT_0080ab50 + local_8 * 4));
      if ((*(uint *)(*(int *)(DAT_0080ab50 + local_8 * 4) + 0xc) & 0x83) == 0) {
        local_c = *(undefined4 **)(DAT_0080ab50 + local_8 * 4);
        goto LAB__text__00577e8e;
      }
      FUN__text__00577320(local_8,*(undefined4 *)(DAT_0080ab50 + local_8 * 4));
    }
    local_8 = local_8 + 1;
  } while( true );
}

