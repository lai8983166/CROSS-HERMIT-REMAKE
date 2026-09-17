
/* WARNING: Instruction at (ram,0x00837816) overlaps instruction at (ram,0x00837815)
    */
/* WARNING: Removing unreachable block (ram,0x00837831) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

HANDLE FUN__text1__0083768a(HWND param_1,UINT param_2,WPARAM param_3,LPARAM param_4)

{
  HANDLE pvVar1;
  BOOL BVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  int unaff_EDI;
  undefined1 local_1020 [4080];
  undefined1 uVar7;
  SIZE_T *lpNumberOfBytesRead;
  int iVar8;
  
  FUN__text1__00848c20();
  if (param_2 == 0x11) {
    if (DAT_00875420 == '\0') {
      pvVar1 = (HANDLE)0x1;
    }
    else {
      SetPropA(param_1,"Shutdown",(HANDLE)0x1);
      EnumThreadWindows(DAT_008753f0[3],FUN__text1__00837ca0,0);
      pvVar1 = GetPropA(param_1,"Shutdown");
    }
  }
  else if (param_2 == 0x16) {
    if (DAT_00875420 == '\0') {
      pvVar1 = (HANDLE)0x1;
    }
    else {
      EnumThreadWindows(DAT_008753f0[3],FUN__text1__00837cd5,(LPARAM)&stack0xfffffff4);
      pvVar1 = (HANDLE)0x0;
    }
  }
  else if (param_2 == 0x113) {
    if (((DAT_0086e3c8 ^ _DAT_0086e3d8 ^ DAT_0086e3ac) & 8) != 0) {
      EnterCriticalSection((LPCRITICAL_SECTION)&DAT_008752c8);
      uVar4 = 1;
      iVar8 = 0;
      for (lpNumberOfBytesRead = (SIZE_T *)0x0; (int)lpNumberOfBytesRead < DAT_00875408;
          lpNumberOfBytesRead = (SIZE_T *)((int)lpNumberOfBytesRead + 1)) {
        iVar3 = (int)lpNumberOfBytesRead * 0x1000;
        if (((*(uint *)(DAT_00875414 + (int)lpNumberOfBytesRead * 4) & 1) != 0) &&
           ((*(uint *)(DAT_00875414 + (int)lpNumberOfBytesRead * 4) & 4) != 0)) {
          lpNumberOfBytesRead = (SIZE_T *)&stack0xffffffe4;
          uVar4 = 0;
          BVar2 = ReadProcessMemory((HANDLE)*DAT_008753f0,(LPCVOID)(DAT_008753f4 + iVar3),local_1020
                                    ,0x1000,lpNumberOfBytesRead);
          if (BVar2 != 0) {
            lpNumberOfBytesRead = (SIZE_T *)0xffffffff;
            uVar4 = 0;
            iVar3 = FUN__text1__00811f90(local_1020,0x1000);
            iVar8 = unaff_EDI;
            if (iVar3 == *(int *)(DAT_00875418 + (int)lpNumberOfBytesRead * 4)) {
              lpNumberOfBytesRead = (SIZE_T *)0x83787f;
              _DAT_00875400 = GetTickCount();
            }
            else {
                    /* WARNING: Ignoring partial resolution of indirect */
              uVar7 = 0;
            }
          }
        }
      }
      if (iVar8 == 0) {
        _DAT_00875400 = GetTickCount();
      }
      if ((uVar4 & 0xff) == 0) {
        for (iVar8 = 0; iVar8 < DAT_00875408; iVar8 = iVar8 + 1) {
          uVar4 = ((((uint)(((int)DAT_008753d8 % 10000) * 0xc45 +
                           ((int)DAT_008753d8 / 10000) * 0x16bd) % 10000) * 10000 +
                   ((int)DAT_008753d8 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
          uVar5 = (((((uVar4 % 10000) * 0xc45 + (uVar4 / 10000) * 0x16bd) % 10000) * 10000 +
                   (uVar4 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
          uVar6 = (((((uVar5 % 10000) * 0xc45 + (uVar5 / 10000) * 0x16bd) % 10000) * 10000 +
                   (uVar5 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
          DAT_008753d8 = (((((uVar6 % 10000) * 0xc45 + (uVar6 / 10000) * 0x16bd) % 10000) * 10000 +
                          (uVar6 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
          *(uint *)(DAT_008753ec + iVar8 * 4) =
               *(uint *)(DAT_008753ec + iVar8 * 4) ^
               (((uVar4 / 10000) * 0x100) / 10000 << 0x18 |
                (((uVar5 / 10000) * 0x100) / 10000 & 0xff) << 0x10 |
                (((uVar6 / 10000) * 0x100) / 10000 & 0xff) << 8 |
               ((DAT_008753d8 / 10000) * 0x100) / 10000 & 0xff);
        }
      }
      LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_008752c8);
    }
    pvVar1 = (HANDLE)0x1;
  }
  else {
    pvVar1 = (HANDLE)DefWindowProcA(param_1,param_2,param_3,param_4);
  }
  return pvVar1;
}

