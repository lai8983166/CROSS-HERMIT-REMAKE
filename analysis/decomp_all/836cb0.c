
undefined4 FUN__text1__00836cb0(char *param_1)

{
  DWORD DVar1;
  undefined4 uVar2;
  char *pcVar3;
  CHAR local_250 [260];
  HANDLE local_14c;
  _WIN32_FIND_DATAA local_148;
  
  DVar1 = GetModuleFileNameA((HMODULE)0x0,local_250,0x104);
  if (DVar1 == 0) {
    uVar2 = 0;
  }
  else {
    local_14c = FindFirstFileA(local_250,&local_148);
    if (local_14c == (HANDLE)0xffffffff) {
      uVar2 = 0;
    }
    else {
      FindClose(local_14c);
      FUN__text1__00848d20(param_1,local_148.cFileName);
      pcVar3 = _strrchr(param_1,0x2e);
      if (pcVar3 != (char *)0x0) {
        *pcVar3 = '\0';
      }
      uVar2 = 1;
    }
  }
  return uVar2;
}

