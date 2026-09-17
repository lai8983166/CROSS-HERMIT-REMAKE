
size_t FUN__text1__0084e79d
                 (LCID param_1,uint param_2,LPCWSTR param_3,int param_4,LPWSTR param_5,
                 size_t param_6,UINT param_7)

{
  int iVar1;
  size_t sVar2;
  int iVar3;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_008743f0;
  puStack_10 = &LAB__text1__00849320;
  local_14 = ExceptionList;
  ExceptionList = &local_14;
  if (DAT_008758dc == 0) {
    ExceptionList = &local_14;
    iVar1 = LCMapStringW(0,0x100,L"",1,(LPWSTR)0x0,0);
    if (iVar1 == 0) {
      iVar1 = LCMapStringA(0,0x100,"",1,(LPSTR)0x0,0);
      if (iVar1 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      DAT_008758dc = 2;
    }
    else {
      DAT_008758dc = 1;
    }
  }
  if (0 < param_4) {
    param_4 = FUN__text1__0084e9a6(param_3,param_4);
  }
  if (DAT_008758dc == 1) {
    sVar2 = LCMapStringW(param_1,param_2,param_3,param_4,param_5,param_6);
    ExceptionList = local_14;
    return sVar2;
  }
  if (DAT_008758dc == 2) {
    if (param_7 == 0) {
      param_7 = DAT_008758cc;
    }
    iVar1 = WideCharToMultiByte(param_7,0x220,param_3,param_4,(LPSTR)0x0,0,(LPCSTR)0x0,(LPBOOL)0x0);
    if (iVar1 != 0) {
      local_8 = 0;
      FUN__text1__00848c20();
      local_8 = 0xffffffff;
      if ((&stack0x00000000 != (undefined1 *)0x3c) &&
         (iVar3 = WideCharToMultiByte(param_7,0x220,param_3,param_4,&stack0xffffffc4,iVar1,
                                      (LPCSTR)0x0,(LPBOOL)0x0), iVar3 != 0)) {
        sVar2 = LCMapStringA(param_1,param_2,&stack0xffffffc4,iVar1,(LPSTR)0x0,0);
        if (sVar2 != 0) {
          local_8 = 1;
          FUN__text1__00848c20();
          local_8 = 0xffffffff;
          if ((&stack0x00000000 != (undefined1 *)0x3c) &&
             (iVar1 = LCMapStringA(param_1,param_2,&stack0xffffffc4,iVar1,&stack0xffffffc4,sVar2),
             iVar1 != 0)) {
            if ((param_2 & 0x400) != 0) {
              if (param_6 != 0) {
                if ((int)sVar2 <= (int)param_6) {
                  param_6 = sVar2;
                }
                _strncpy((char *)param_5,&stack0xffffffc4,param_6);
                ExceptionList = local_14;
                return sVar2;
              }
              ExceptionList = local_14;
              return sVar2;
            }
            if (param_6 == 0) {
              param_6 = 0;
              param_5 = (LPWSTR)0x0;
            }
            sVar2 = MultiByteToWideChar(param_7,1,&stack0xffffffc4,sVar2,param_5,param_6);
            if (sVar2 != 0) {
              ExceptionList = local_14;
              return sVar2;
            }
          }
        }
      }
    }
  }
  ExceptionList = local_14;
  return 0;
}

