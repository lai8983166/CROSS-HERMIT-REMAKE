
/* WARNING: Removing unreachable block (ram,0x00833808) */

void FUN__text1__008334df(void)

{
  char cVar1;
  BOOL BVar2;
  DWORD DVar3;
  void *_Dst;
  char *_Str;
  int iVar4;
  HGLOBAL pvVar5;
  LPVOID pvVar6;
  LPARAM LVar7;
  size_t sVar8;
  tagMSG local_24;
  DWORD local_8;
  
  DAT_00874840 = (HWND)FUN__text1__00833939();
  local_8 = GetTickCount();
  do {
    while( true ) {
      while( true ) {
        while (BVar2 = PeekMessageA(&local_24,DAT_00874840,0,0,1), BVar2 != 0) {
          TranslateMessage(&local_24);
          DispatchMessageA(&local_24);
        }
        if ((DAT_00874848 != 0) && (DVar3 = GetTickCount(), local_8 + 500 < DVar3)) break;
        Sleep(1);
      }
      local_8 = GetTickCount();
      if (DAT_00874844 != (HWND)0x0) break;
      EnumWindows(FUN__text1__00833849,0);
    }
    BVar2 = IsWindow(DAT_00874844);
    if (BVar2 == 0) {
      DAT_00874844 = (HWND)0x0;
    }
    else {
      _Dst = operator_new(0x20000);
      _memset(_Dst,0,0x20000);
      _Str = operator_new(0x10000);
      _memset(_Str,0,0x10000);
      cVar1 = FUN__text1__0083309d();
      if (cVar1 == '\0') {
        while (cVar1 = FUN__text1__008331bc(_Str,0x10000), cVar1 != '\0') {
          sVar8 = _strlen(_Str);
          pvVar5 = GlobalAlloc(0x2002,sVar8 + 1);
          pvVar6 = GlobalLock(pvVar5);
          FUN__text1__00848d20(pvVar6,_Str);
          GlobalUnlock(pvVar5);
          LVar7 = PackDDElParam(1000,0,(UINT_PTR)pvVar5);
          PostMessageA(DAT_00874844,1000,(WPARAM)DAT_00874840,LVar7);
        }
      }
      else {
        while (cVar1 = FUN__text1__00833387(_Dst,0x10000), cVar1 != '\0') {
          BVar2 = IsWindowUnicode(DAT_00874844);
          if (BVar2 == 0) {
            FUN__text1__00833810(_Dst,_Str,0x10000);
            sVar8 = _strlen(_Str);
            pvVar5 = GlobalAlloc(0x2002,sVar8 + 1);
            pvVar6 = GlobalLock(pvVar5);
            FUN__text1__00848d20(pvVar6,_Str);
            GlobalUnlock(pvVar5);
            LVar7 = PackDDElParam(1000,0,(UINT_PTR)pvVar5);
            PostMessageA(DAT_00874844,1000,(WPARAM)DAT_00874840,LVar7);
          }
          else {
            iVar4 = FUN__text1__0084904e(_Dst);
            pvVar5 = GlobalAlloc(0x2002,iVar4 * 2 + 1);
            pvVar6 = GlobalLock(pvVar5);
            FUN__text1__00848e60(pvVar6,_Dst);
            GlobalUnlock(pvVar5);
            LVar7 = PackDDElParam(1000,0,(UINT_PTR)pvVar5);
            PostMessageW(DAT_00874844,1000,(WPARAM)DAT_00874840,LVar7);
          }
        }
      }
      FUN__text1__00848476(_Str);
      FUN__text1__00848476(_Dst);
    }
  } while( true );
}

