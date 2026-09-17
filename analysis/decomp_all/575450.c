
void FUN__text__00575450(int param_1)

{
  if (DAT_00761bc0 != -1) {
    if (param_1 == 0) {
      param_1 = (*API_KERNEL32_DLL_TlsGetValue)(DAT_00761bc0);
    }
    if (param_1 != 0) {
      if (*(int *)(param_1 + 0x24) != 0) {
        __free_dbg(*(undefined4 *)(param_1 + 0x24),2);
      }
      if (*(int *)(param_1 + 0x28) != 0) {
        __free_dbg(*(undefined4 *)(param_1 + 0x28),2);
      }
      if (*(int *)(param_1 + 0x30) != 0) {
        __free_dbg(*(undefined4 *)(param_1 + 0x30),2);
      }
      if (*(int *)(param_1 + 0x38) != 0) {
        __free_dbg(*(undefined4 *)(param_1 + 0x38),2);
      }
      if (*(int *)(param_1 + 0x40) != 0) {
        __free_dbg(*(undefined4 *)(param_1 + 0x40),2);
      }
      if (*(int *)(param_1 + 0x44) != 0) {
        __free_dbg(*(undefined4 *)(param_1 + 0x44),2);
      }
      if (*(undefined **)(param_1 + 0x50) != &DAT_00761d68) {
        __free_dbg(*(undefined4 *)(param_1 + 0x50),2);
      }
      __free_dbg(param_1,2);
    }
    (*API_KERNEL32_DLL_TlsSetValue)(DAT_00761bc0,0);
  }
  return;
}

