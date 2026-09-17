
int FUN__text1__0083586e(void)

{
  int iVar1;
  DWORD DVar2;
  CHAR local_114 [256];
  FARPROC local_14;
  HMODULE local_10;
  undefined1 local_c;
  int local_8;
  
  local_c = 0;
  local_10 = LoadLibraryA("Kernel32");
  if (local_10 != (HMODULE)0x0) {
    local_14 = GetProcAddress(local_10,"IsDebuggerPresent");
    if (local_14 != (FARPROC)0x0) {
      iVar1 = (*local_14)();
      if (iVar1 != 0) {
        DVar2 = GetCurrentProcessId();
        FUN__text1__008491aa(local_114,"%X:DAF",DVar2);
        CreateMutexA((LPSECURITY_ATTRIBUTES)0x0,0,local_114);
      }
    }
  }
  FUN__text1__008491fc(FUN__text1__00833fac);
  local_8 = FUN__text1__00833fdb();
  FUN__text1__008491fc(0);
  if (local_8 == 1) {
    (*DAT_00874ec0)(&DAT_00874e98);
  }
  return local_8;
}

