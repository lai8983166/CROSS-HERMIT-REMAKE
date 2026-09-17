
void FUN__text1__00836190(void)

{
  DWORD DVar1;
  BOOL BVar2;
  int local_8;
  
  DVar1 = GetCurrentThreadId();
  if (DAT_00875210 == DVar1) {
    DestroyWindow((HWND)PTR_DAT_00875200);
    PTR_DAT_00875200 = (undefined *)0x0;
  }
  else {
    PostMessageA((HWND)PTR_DAT_00875200,0x40a,0,0);
    local_8 = 0;
    while ((local_8 < 0x14 && (BVar2 = IsWindow((HWND)PTR_DAT_00875200), BVar2 != 0))) {
      Sleep(100);
      local_8 = local_8 + 1;
    }
  }
  return;
}

