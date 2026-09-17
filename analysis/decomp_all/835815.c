
void FUN__text1__00835815(uint param_1)

{
  if (DAT_008751e0 == (FARPROC)0x0) {
    DAT_008751dc = LoadLibraryA("KERNEL32.DLL");
    DAT_008751e0 = GetProcAddress(DAT_008751dc,"RegisterServiceProcess");
  }
  if (DAT_008751e0 != (FARPROC)0x0) {
    (*DAT_008751e0)(0,param_1 & 0xff);
  }
  return;
}

