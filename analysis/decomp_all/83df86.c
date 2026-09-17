
void FUN__text1__0083df86(void)

{
  undefined4 local_1c;
  undefined4 local_18;
  HWND local_14;
  undefined4 local_10;
  FARPROC local_c;
  HMODULE local_8;
  
  local_8 = LoadLibraryA("COMCTL32.DLL");
  if (local_8 != (HMODULE)0x0) {
    local_c = GetProcAddress(local_8,"_TrackMouseEvent");
    if (local_c != (FARPROC)0x0) {
      local_1c = 0x10;
      local_18 = 0x40000000;
      local_14 = GetDesktopWindow();
      local_10 = 0xffffffff;
      (*local_c)(&local_1c);
    }
  }
  return;
}

