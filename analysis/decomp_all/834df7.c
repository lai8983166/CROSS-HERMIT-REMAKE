
undefined4 FUN__text1__00834df7(int param_1,int param_2)

{
  LPCSTR lpProcName;
  uint uVar1;
  LPCSTR lpLibFileName;
  HMODULE hModule;
  DWORD DVar2;
  FARPROC local_20;
  undefined4 *local_18;
  uint *local_14;
  int *local_8;
  
  if (param_2 != 0) {
    for (local_8 = (int *)(param_2 + param_1); local_8[3] != 0; local_8 = local_8 + 5) {
      lpLibFileName = (LPCSTR)(local_8[3] + param_1);
      local_14 = (uint *)(*local_8 + param_1);
      local_18 = (undefined4 *)(local_8[4] + param_1);
      SetLastError(0);
      hModule = LoadLibraryA(lpLibFileName);
      if (hModule == (HMODULE)0x0) {
        DAT_008750d8 = 3;
        DVar2 = GetLastError();
        FUN__text1__008491aa(&DAT_008750dc,"File \"%s\", error %d",lpLibFileName,DVar2);
        return 0;
      }
      for (; *local_14 != 0; local_14 = local_14 + 1) {
        if ((*local_14 & 0x80000000) == 0) {
          lpProcName = (LPCSTR)(*local_14 + 2 + param_1);
          local_20 = GetProcAddress(hModule,lpProcName);
          if (local_20 == (FARPROC)0x0) {
            DAT_008750d8 = 3;
            FUN__text1__008491aa
                      (&DAT_008750dc,"File \"%s\", function \"%s\"",lpLibFileName,lpProcName);
            return 0;
          }
        }
        else {
          uVar1 = *local_14;
          local_20 = GetProcAddress(hModule,(LPCSTR)(uVar1 & 0xffff));
          if (local_20 == (FARPROC)0x0) {
            DAT_008750d8 = 3;
            FUN__text1__008491aa
                      (&DAT_008750dc,"File \"%s\", ordinal %d",lpLibFileName,uVar1 & 0xffff);
            return 0;
          }
        }
        *local_18 = local_20;
        local_18 = local_18 + 1;
      }
    }
  }
  return 1;
}

