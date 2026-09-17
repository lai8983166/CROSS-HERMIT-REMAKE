
undefined4 * __fastcall FUN__text1__00832d09(undefined4 *param_1)

{
  char cVar1;
  DWORD DVar2;
  undefined2 *puVar3;
  char *pcVar4;
  int iVar5;
  undefined4 *puVar6;
  char *local_32c;
  char *local_328;
  WCHAR *local_324;
  WCHAR *local_320;
  CHAR local_318;
  undefined4 local_317;
  char *local_214;
  WCHAR local_210;
  undefined4 local_20e [129];
  undefined2 *local_8;
  
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  InitializeCriticalSection((LPCRITICAL_SECTION)(param_1 + 4));
  DVar2 = GetCurrentProcessId();
  param_1[10] = DVar2;
  cVar1 = FUN__text1__0083309d();
  if (cVar1 == '\0') {
    local_318 = DAT_00874e88;
    puVar6 = &local_317;
    for (iVar5 = 0x40; iVar5 != 0; iVar5 = iVar5 + -1) {
      *puVar6 = 0;
      puVar6 = puVar6 + 1;
    }
    *(undefined2 *)puVar6 = 0;
    *(undefined1 *)((int)puVar6 + 2) = 0;
    GetModuleFileNameA((HMODULE)0x0,&local_318,0x104);
    local_214 = _strrchr(&local_318,0x5c);
    if (local_214 == (char *)0x0) {
      local_328 = &local_318;
    }
    else {
      local_328 = local_214 + 1;
    }
    FUN__text1__00848d20(param_1 + 0xb,local_328);
    local_214 = _strchr((char *)(param_1 + 0xb),0x2e);
    if (local_214 != (char *)0x0) {
      *local_214 = '\0';
    }
    GetModuleFileNameA((HMODULE)0x0,(LPSTR)(param_1 + 0x4c),0x104);
    DVar2 = GetShortPathNameA((LPCSTR)(param_1 + 0x4c),&local_318,0x104);
    if (DVar2 == 0) {
      FUN__text1__00848d20(param_1 + 0x4c,&DAT_00874e88);
    }
    else {
      local_214 = _strrchr(&local_318,0x5c);
      if (local_214 == (char *)0x0) {
        local_32c = &local_318;
      }
      else {
        local_32c = local_214 + 1;
      }
      FUN__text1__00848d20(param_1 + 0x4c,local_32c);
      pcVar4 = _strchr((char *)(param_1 + 0x4c),0x2e);
      if (pcVar4 != (char *)0x0) {
        *pcVar4 = '\0';
      }
    }
  }
  else {
    local_210 = DAT_00874e8c;
    puVar6 = local_20e;
    for (iVar5 = 0x81; iVar5 != 0; iVar5 = iVar5 + -1) {
      *puVar6 = 0;
      puVar6 = puVar6 + 1;
    }
    *(undefined2 *)puVar6 = 0;
    GetModuleFileNameW((HMODULE)0x0,&local_210,0x104);
    local_8 = (undefined2 *)FUN__text1__00848e85(&local_210,0x5c);
    if (local_8 == (undefined2 *)0x0) {
      local_320 = &local_210;
    }
    else {
      local_320 = (WCHAR *)((int)local_8 + 2);
    }
    FUN__text1__00848e60(param_1 + 0x8d,local_320);
    local_8 = (undefined2 *)FUN__text1__00848e37(param_1 + 0x8d,0x2e);
    if (local_8 != (undefined2 *)0x0) {
      *local_8 = 0;
    }
    GetModuleFileNameW((HMODULE)0x0,(LPWSTR)(param_1 + 0x10f),0x104);
    DVar2 = GetShortPathNameW((LPCWSTR)(param_1 + 0x10f),&local_210,0x104);
    if (DVar2 == 0) {
      FUN__text1__00848e60(param_1 + 0x10f,&DAT_00874e8c);
    }
    else {
      local_8 = (undefined2 *)FUN__text1__00848e85(&local_210,0x5c);
      if (local_8 == (undefined2 *)0x0) {
        local_324 = &local_210;
      }
      else {
        local_324 = (WCHAR *)((int)local_8 + 2);
      }
      FUN__text1__00848e60(param_1 + 0x10f,local_324);
      puVar3 = (undefined2 *)FUN__text1__00848e37(param_1 + 0x10f,0x2e);
      if (puVar3 != (undefined2 *)0x0) {
        *puVar3 = 0;
      }
    }
  }
  return param_1;
}

