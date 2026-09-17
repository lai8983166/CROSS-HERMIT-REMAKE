
LRESULT FUN__text1__00833aa4(HWND param_1,UINT param_2,HWND param_3,HGLOBAL param_4)

{
  char cVar1;
  ATOM AVar2;
  size_t sVar3;
  LPARAM LVar4;
  BOOL BVar5;
  LPVOID pvVar6;
  WPARAM wParam;
  LRESULT LVar7;
  int iVar8;
  undefined4 *puVar9;
  HGLOBAL local_620;
  uint local_61c;
  LPVOID local_618;
  LPVOID local_614;
  CHAR local_610;
  undefined4 local_60f;
  CHAR local_510;
  undefined4 local_50f;
  WCHAR local_410;
  undefined4 local_40e [127];
  WCHAR local_210;
  undefined4 local_20e [127];
  int local_10;
  uint local_c;
  HWND local_8;
  
  AVar2 = (ATOM)((uint)param_4 >> 0x10);
  switch(param_2) {
  case 0x3e0:
    local_8 = param_3;
    local_c = CONCAT22(local_c._2_2_,(ATOM)param_4);
    local_10 = CONCAT22(local_10._2_2_,AVar2);
    cVar1 = FUN__text1__0083309d();
    if (cVar1 == '\0') {
      local_510 = DAT_00874e88;
      puVar9 = &local_50f;
      for (iVar8 = 0x3f; iVar8 != 0; iVar8 = iVar8 + -1) {
        *puVar9 = 0;
        puVar9 = puVar9 + 1;
      }
      *(undefined2 *)puVar9 = 0;
      *(undefined1 *)((int)puVar9 + 2) = 0;
      local_610 = DAT_00874e88;
      puVar9 = &local_60f;
      for (iVar8 = 0x3f; iVar8 != 0; iVar8 = iVar8 + -1) {
        *puVar9 = 0;
        puVar9 = puVar9 + 1;
      }
      *(undefined2 *)puVar9 = 0;
      *(undefined1 *)((int)puVar9 + 2) = 0;
      GlobalGetAtomNameA((ATOM)local_c,&local_510,0x100);
      GlobalGetAtomNameA((ATOM)local_10,&local_610,0x100);
      sVar3 = _strlen(&local_510);
      if ((sVar3 != 0) &&
         (((iVar8 = __strcmpi(&local_510,""), iVar8 == 0 ||
           (iVar8 = __strcmpi(&local_510,""), iVar8 == 0)) &&
          (iVar8 = __strcmpi(&local_610,"System"), iVar8 == 0)))) {
        GlobalDeleteAtom((ATOM)local_c);
        GlobalDeleteAtom((ATOM)local_10);
        AVar2 = GlobalAddAtomA(&local_510);
        local_c = CONCAT22(local_c._2_2_,AVar2);
        AVar2 = GlobalAddAtomA(&local_610);
        local_10 = CONCAT22(local_10._2_2_,AVar2);
        SendMessageA(local_8,0x3e4,(WPARAM)param_1,local_c & 0xffff | local_10 << 0x10);
      }
    }
    else {
      local_210 = DAT_00874e8c;
      puVar9 = local_20e;
      for (iVar8 = 0x7f; iVar8 != 0; iVar8 = iVar8 + -1) {
        *puVar9 = 0;
        puVar9 = puVar9 + 1;
      }
      *(undefined2 *)puVar9 = 0;
      local_410 = DAT_00874e8c;
      puVar9 = local_40e;
      for (iVar8 = 0x7f; iVar8 != 0; iVar8 = iVar8 + -1) {
        *puVar9 = 0;
        puVar9 = puVar9 + 1;
      }
      *(undefined2 *)puVar9 = 0;
      GlobalGetAtomNameW((ATOM)local_c,&local_210,0x100);
      GlobalGetAtomNameW((ATOM)local_10,&local_410,0x100);
      iVar8 = FUN__text1__0084904e(&local_210);
      if (((iVar8 != 0) &&
          ((iVar8 = FUN__text1__0084e52c(&local_210,L"CROSS HERMIT"), iVar8 == 0 ||
           (iVar8 = FUN__text1__0084e52c(&local_210,L"CROSS HERMIT"), iVar8 == 0)))) &&
         (iVar8 = FUN__text1__0084e52c(&local_410,L"System"), iVar8 == 0)) {
        GlobalDeleteAtom((ATOM)local_c);
        GlobalDeleteAtom((ATOM)local_10);
        AVar2 = GlobalAddAtomW(&local_210);
        local_c = CONCAT22(local_c._2_2_,AVar2);
        AVar2 = GlobalAddAtomW(&local_410);
        local_10 = CONCAT22(local_10._2_2_,AVar2);
        SendMessageW(local_8,0x3e4,(WPARAM)param_1,local_c & 0xffff | local_10 << 0x10);
      }
    }
    LVar7 = 0;
    break;
  case 0x3e1:
    LVar4 = 0;
    wParam = PackDDElParam(0x3e1,(UINT_PTR)param_1,0);
    PostMessageA(param_3,0x3e1,wParam,LVar4);
    LVar7 = 0;
    break;
  default:
    LVar7 = DefWindowProcA(param_1,param_2,(WPARAM)param_3,(LPARAM)param_4);
    break;
  case 0x3e4:
    BVar5 = InSendMessage();
    if (BVar5 == 0) {
      UnpackDDElParam(0x3e4,(LPARAM)param_4,&local_61c,(PUINT_PTR)&local_620);
      if ((local_61c & 0x8000) == 0) {
        cVar1 = FUN__text1__0083309d();
        if (cVar1 == '\0') {
          pvVar6 = GlobalLock(local_620);
          FUN__text1__008330ea(pvVar6);
          GlobalUnlock(local_620);
        }
        else {
          pvVar6 = GlobalLock(local_620);
          FUN__text1__008332b3(pvVar6);
          GlobalUnlock(local_620);
        }
      }
      FreeDDElParam(0x3e4,(LPARAM)param_4);
      GlobalFree(local_620);
    }
    else {
      DAT_00874844 = param_3;
      GlobalDeleteAtom((ATOM)param_4);
      GlobalDeleteAtom(AVar2);
    }
    LVar7 = 0;
    break;
  case 1000:
    cVar1 = FUN__text1__0083309d();
    if (cVar1 == '\0') {
      local_618 = GlobalLock(param_4);
      FUN__text1__008330ea(local_618);
      GlobalUnlock(param_4);
    }
    else {
      local_614 = GlobalLock(param_4);
      FUN__text1__008332b3(local_614);
      GlobalUnlock(param_4);
    }
    LVar4 = PackDDElParam(0x3e4,0x8000,(UINT_PTR)param_4);
    PostMessageA(param_3,0x3e4,(WPARAM)param_1,LVar4);
    LVar7 = 0;
  }
  return LVar7;
}

