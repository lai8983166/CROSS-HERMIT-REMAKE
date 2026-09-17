
undefined1 FUN__text1__0083309d(void)

{
  _OSVERSIONINFOA local_98;
  
  if (DAT_00874e85 == '\0') {
    local_98.dwOSVersionInfoSize = 0x94;
    GetVersionExA(&local_98);
    DAT_00874e84 = local_98.dwPlatformId == 2;
    DAT_00874e85 = '\x01';
  }
  return DAT_00874e84;
}

