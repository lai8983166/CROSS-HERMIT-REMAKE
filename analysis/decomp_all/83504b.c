
/* WARNING: Instruction at (ram,0x00835615) overlaps instruction at (ram,0x00835614)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Removing unreachable block (ram,0x008356c1) */
/* WARNING: Removing unreachable block (ram,0x00835615) */
/* WARNING: Removing unreachable block (ram,0x00835675) */
/* WARNING: Removing unreachable block (ram,0x0083562b) */
/* WARNING: Removing unreachable block (ram,0x00835691) */
/* WARNING: Removing unreachable block (ram,0x00835685) */
/* WARNING: Removing unreachable block (ram,0x00835692) */
/* WARNING: Removing unreachable block (ram,0x00835639) */
/* WARNING: Heritage AFTER dead removal. Example location: s0xfffff954 : 0x008356df */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: stack */
/* WARNING: Exceeded maximum restarts with more pending */

int FUN__text1__0083504b(void)

{
  char cVar1;
  HANDLE pvVar2;
  DWORD DVar3;
  size_t sVar4;
  LPSTR lpCommandLine;
  FARPROC pFVar5;
  int iVar6;
  undefined4 unaff_EDI;
  undefined4 *puVar7;
  LPSECURITY_ATTRIBUTES lpProcessAttributes;
  LPSECURITY_ATTRIBUTES lpThreadAttributes;
  BOOL BVar8;
  LPVOID lpEnvironment;
  LPCSTR lpCurrentDirectory;
  _STARTUPINFOA *lpStartupInfo;
  undefined2 uVar9;
  _PROCESS_INFORMATION *lpProcessInformation;
  undefined2 uVar10;
  undefined2 uStack_75c;
  undefined2 uStack_75a;
  _OSVERSIONINFOA local_744;
  HMODULE local_6b0;
  uint local_6ac;
  CHAR local_6a8;
  undefined4 local_6a7;
  _STARTUPINFOA local_5a4;
  CHAR local_560;
  undefined4 local_55f;
  _PROCESS_INFORMATION local_45c;
  int local_44c;
  CHAR local_448 [256];
  CHAR local_348 [200];
  undefined1 local_280;
  uint local_148;
  int local_144;
  char *local_140;
  int local_13c;
  HWND local_138;
  DWORD local_134;
  HANDLE local_130;
  CHAR local_12c [260];
  uint local_28;
  code *local_24;
  int local_20;
  undefined1 *local_1c;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_00872da0;
  puStack_10 = &LAB__text1__00849320;
  local_14 = ExceptionList;
  local_1c = (undefined1 *)&uStack_75c;
  uStack_75c = (undefined2)unaff_EDI;
  uStack_75a = (undefined2)((uint)unaff_EDI >> 0x10);
  local_28 = CONCAT31(local_28._1_3_,1);
  local_24 = LoadStringW_exref + 1;
  ExceptionList = &local_14;
  FUN__text1__008491fc();
  GetCurrentProcessId();
  FUN__text1__008491aa();
  pvVar2 = OpenMutexA(0x1f0001,0,local_12c);
  if (pvVar2 != (HANDLE)0x0) {
    local_28 = local_28 & 0xffffff00;
  }
  if (((local_28 & 0xff) != 0) && (((DAT_0086e3c8 ^ _DAT_0086e3d8 ^ DAT_0086e3ac) & 0x20) != 0)) {
    FUN__text1__008491aa();
    local_130 = CreateMutexA((LPSECURITY_ATTRIBUTES)0x0,0,local_12c);
    if ((local_130 != (HANDLE)0x0) && (DVar3 = GetLastError(), DVar3 == 0xb7)) {
      local_134 = WaitForSingleObject(local_130,30000);
      if ((local_134 == 0) || (local_134 == 0x80)) {
        FUN__text1__008491aa();
        local_13c = 0;
        while ((local_13c < 300 &&
               (local_138 = FindWindowA("MainClass",local_12c), local_138 == (HWND)0x0))) {
          Sleep(100);
          local_13c = local_13c + 1;
        }
        if (local_138 != (HWND)0x0) {
          local_148 = DAT_0086e3e4 ^ _DAT_0086e3f0 ^ DAT_0086e3f4;
          sVar4 = _strlen(DAT_00874ea0);
          local_144 = sVar4 + 1;
          local_140 = DAT_00874ea0;
          SendMessageA(local_138,0x4a,0,(LPARAM)&local_148);
        }
        ReleaseMutex(local_130);
      }
      ExceptionList = local_14;
      return 1;
    }
  }
  FUN__text1__00835815();
  if ((((local_28 & 0xff) != 0) && (((DAT_0086e3c8 ^ _DAT_0086e3d8 ^ DAT_0086e3ac) & 0x40) == 0)) &&
     (DVar3 = GetEnvironmentVariableA("_PAD64",local_348,0x200), DVar3 == 0)) {
    _memset(local_348,0x23,200);
    local_280 = 0;
    for (local_44c = 1; local_44c < 0x41; local_44c = local_44c + 1) {
      FUN__text1__008491aa();
      SetEnvironmentVariableA(local_448,local_348);
    }
    if (((DAT_0086e3c8 ^ _DAT_0086e3d8 ^ DAT_0086e3ac) & 0x10) == 0) {
      GetStartupInfoA(&local_5a4);
      local_6a8 = DAT_00874e88;
      puVar7 = &local_6a7;
      for (iVar6 = 0x40; iVar6 != 0; iVar6 = iVar6 + -1) {
        *puVar7 = 0;
        puVar7 = puVar7 + 1;
      }
      *(undefined2 *)puVar7 = 0;
      *(undefined1 *)((int)puVar7 + 2) = 0;
      local_560 = DAT_00874e88;
      puVar7 = &local_55f;
      for (iVar6 = 0x40; iVar6 != 0; iVar6 = iVar6 + -1) {
        *puVar7 = 0;
        puVar7 = puVar7 + 1;
      }
      *(undefined2 *)puVar7 = 0;
      *(undefined1 *)((int)puVar7 + 2) = 0;
      if (((DAT_00874e98 == 1) && (local_5a4.lpTitle == (CHAR *)0x0)) &&
         (cVar1 = FUN__text1__00836cb0(), cVar1 != '\0')) {
        local_5a4.lpTitle = &local_6a8;
      }
      DVar3 = GetModuleFileNameA((HMODULE)0x0,&local_560,0x104);
      if (DVar3 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      lpProcessInformation = &local_45c;
      lpStartupInfo = &local_5a4;
      lpCurrentDirectory = (LPCSTR)0x0;
      lpEnvironment = (LPVOID)0x0;
      DVar3 = 0;
      BVar8 = 0;
      lpThreadAttributes = (LPSECURITY_ATTRIBUTES)0x0;
      lpProcessAttributes = (LPSECURITY_ATTRIBUTES)0x0;
      lpCommandLine = GetCommandLineA();
      BVar8 = CreateProcessA(&local_560,lpCommandLine,lpProcessAttributes,lpThreadAttributes,BVar8,
                             DVar3,lpEnvironment,lpCurrentDirectory,lpStartupInfo,
                             lpProcessInformation);
      if (BVar8 == 0) {
        DAT_008750d8 = 6;
        GetLastError();
        FUN__text1__008491aa();
        ExceptionList = local_14;
        return 0;
      }
      WaitForInputIdle(local_45c.hProcess,10000);
      ExceptionList = local_14;
      return 1;
    }
  }
  if (((DAT_0086e3c8 ^ _DAT_0086e3d8 ^ DAT_0086e3ac) & 0x10) == 0) {
    if (((DAT_0086e380 ^ _DAT_0086e3d8 ^ DAT_0086e3ac) & 2) != 0) {
      FUN__text1__00833482();
    }
    goto LAB__text1__00835799;
  }
  GetCurrentProcessId();
  FUN__text1__008491aa();
  pvVar2 = OpenMutexA(0x1f0001,0,local_12c);
  if (pvVar2 != (HANDLE)0x0) goto LAB__text1__00835799;
  uVar9 = 1;
  uVar10 = 0;
  pvVar2 = GetCurrentThread();
  SetThreadPriority(pvVar2,CONCAT22(uVar10,uVar9));
  local_6ac = local_6ac & 0xffffff00;
  local_6b0 = LoadLibraryA("Kernel32");
  if (((local_6b0 != (HMODULE)0x0) &&
      (pFVar5 = GetProcAddress(local_6b0,"IsDebuggerPresent"), pFVar5 != (FARPROC)0x0)) &&
     (iVar6 = (*pFVar5)(), iVar6 != 0)) {
    local_6ac = CONCAT31(local_6ac._1_3_,1);
  }
  local_744.dwOSVersionInfoSize = 0x94;
  GetVersionExA(&local_744);
  if (local_744.dwPlatformId == 2) {
    if (*(char *)((int)ProcessEnvironmentBlock + 2) != '\0') {
LAB__text1__0083566e:
      UNK_008750c4 = 1;
    }
  }
  else {
    local_8 = 0xffffffff;
    DAT_008753e0 = 1;
    if (ClientId.UniqueProcess != (void *)0x0) goto LAB__text1__0083566e;
  }
  if ((local_6ac & 0xff) == 0) {
    cVar1 = FUN__text1__00837ea8();
    if (cVar1 == '\0') {
      DAT_008750d8 = 6;
      GetLastError();
      FUN__text1__008491aa();
      ExceptionList = local_14;
      return 0;
    }
    FUN__text1__00835815();
    ExceptionList = local_14;
    return 1;
  }
  GetCurrentProcessId();
  FUN__text1__008491aa();
  CreateMutexA((LPSECURITY_ATTRIBUTES)0x0,0,local_12c);
LAB__text1__00835799:
  local_20 = FUN__text1__00833fdb();
  FUN__text1__00835815();
  FUN__text1__008491fc();
  if (local_20 == 1) {
    local_20 = (*DAT_00874ec0)();
  }
  FUN__text1__008491fc();
  if (DAT_00874ebc != (code *)0x0) {
    (*DAT_00874ebc)();
  }
  if (DAT_008750d0 != (code *)0x0) {
    (*DAT_008750d0)();
  }
  ExceptionList = local_14;
  return local_20;
}

