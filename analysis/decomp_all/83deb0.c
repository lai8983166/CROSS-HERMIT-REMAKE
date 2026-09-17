
void FUN__text1__0083deb0(void)

{
  FARPROC pFVar1;
  undefined4 local_6c;
  undefined4 local_68;
  HMODULE local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_20;
  undefined4 *local_18;
  code *local_14;
  
  _memset(&local_38,0,0x34);
  local_38 = 0x34;
  local_34 = 0x108;
  local_20 = 1;
  local_18 = &local_6c;
  local_14 = FUN__text1__0083df40;
  _memset(&local_6c,0,0x30);
  local_6c = 0x30;
  local_68 = 0;
  local_3c = LoadLibraryA("COMCTL32.DLL");
  if (local_3c != (HMODULE)0x0) {
    pFVar1 = GetProcAddress(local_3c,"PropertySheetA");
    if (pFVar1 != (FARPROC)0x0) {
      (*pFVar1)(&local_38);
    }
  }
  return;
}

