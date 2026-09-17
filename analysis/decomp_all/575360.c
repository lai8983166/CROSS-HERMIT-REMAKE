
void FUN__text__00575360(void)

{
  FUN__text__00576fa0();
  if (DAT_00761bc0 != -1) {
    (*API_KERNEL32_DLL_TlsFree)(DAT_00761bc0);
    DAT_00761bc0 = -1;
  }
  return;
}

