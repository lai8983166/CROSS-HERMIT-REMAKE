
undefined4 FUN__text1__0084db38(void)

{
  LPCWSTR lpWideCharStr;
  size_t _Size;
  LPSTR lpMultiByteStr;
  int iVar1;
  undefined4 *puVar2;
  
  lpWideCharStr = (LPCWSTR)*DAT_0087567c;
  puVar2 = DAT_0087567c;
  while( true ) {
    if (lpWideCharStr == (LPCWSTR)0x0) {
      return 0;
    }
    _Size = WideCharToMultiByte(1,0,lpWideCharStr,-1,(LPSTR)0x0,0,(LPCSTR)0x0,(LPBOOL)0x0);
    if (((_Size == 0) || (lpMultiByteStr = _malloc(_Size), lpMultiByteStr == (LPSTR)0x0)) ||
       (iVar1 = WideCharToMultiByte(1,0,(LPCWSTR)*puVar2,-1,lpMultiByteStr,_Size,(LPCSTR)0x0,
                                    (LPBOOL)0x0), iVar1 == 0)) break;
    FUN__text1__0084df01(lpMultiByteStr,0);
    lpWideCharStr = (LPCWSTR)puVar2[1];
    puVar2 = puVar2 + 1;
  }
  return 0xffffffff;
}

