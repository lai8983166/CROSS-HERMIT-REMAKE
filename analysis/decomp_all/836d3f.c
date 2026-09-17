
undefined4 FUN__text1__00836d3f(undefined4 param_1)

{
  DWORD DVar1;
  undefined4 uVar2;
  undefined2 *puVar3;
  WCHAR local_464 [260];
  HANDLE local_25c;
  _WIN32_FIND_DATAW local_258;
  
  DVar1 = GetModuleFileNameW((HMODULE)0x0,local_464,0x104);
  if (DVar1 == 0) {
    uVar2 = 0;
  }
  else {
    local_25c = FindFirstFileW(local_464,&local_258);
    if (local_25c == (HANDLE)0xffffffff) {
      uVar2 = 0;
    }
    else {
      FindClose(local_25c);
      FUN__text1__00848e60(param_1,local_258.cFileName);
      puVar3 = (undefined2 *)FUN__text1__00848e85(param_1,0x2e);
      if (puVar3 != (undefined2 *)0x0) {
        *puVar3 = 0;
      }
      uVar2 = 1;
    }
  }
  return uVar2;
}

