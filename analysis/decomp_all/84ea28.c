
BOOL FUN__text1__0084ea28
               (DWORD param_1,LPCWSTR param_2,int param_3,LPWORD param_4,UINT param_5,LCID param_6)

{
  undefined1 *puVar1;
  BOOL BVar2;
  size_t _Size;
  int iVar3;
  WORD local_20 [2];
  undefined1 *local_1c;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_00874408;
  puStack_10 = &LAB__text1__00849320;
  local_14 = ExceptionList;
  local_1c = &stack0xffffffc4;
  iVar3 = DAT_008758e0;
  ExceptionList = &local_14;
  puVar1 = &stack0xffffffc4;
  if (DAT_008758e0 == 0) {
    ExceptionList = &local_14;
    BVar2 = GetStringTypeW(1,L"",1,local_20);
    iVar3 = 1;
    puVar1 = local_1c;
    if (BVar2 == 0) {
      BVar2 = GetStringTypeA(0,1,"",1,local_20);
      if (BVar2 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      iVar3 = 2;
      puVar1 = local_1c;
    }
  }
  local_1c = puVar1;
  DAT_008758e0 = iVar3;
  if (DAT_008758e0 != 1) {
    if (DAT_008758e0 == 2) {
      if (param_5 == 0) {
        param_5 = DAT_008758cc;
      }
      _Size = WideCharToMultiByte(param_5,0x220,param_2,param_3,(LPSTR)0x0,0,(LPCSTR)0x0,(LPBOOL)0x0
                                 );
      if (_Size != 0) {
        local_8 = 0;
        FUN__text1__00848c20();
        local_1c = &stack0xffffffc4;
        _memset(&stack0xffffffc4,0,_Size);
        local_8 = 0xffffffff;
        if (&stack0x00000000 != (undefined1 *)0x3c) {
          iVar3 = WideCharToMultiByte(param_5,0x220,param_2,param_3,&stack0xffffffc4,_Size,
                                      (LPCSTR)0x0,(LPBOOL)0x0);
          if (iVar3 != 0) {
            local_8 = 1;
            FUN__text1__00848c20();
            local_8 = 0xffffffff;
            if (&stack0x00000000 != (undefined1 *)0x3c) {
              if (param_6 == 0) {
                param_6 = DAT_008758bc;
              }
              local_1c = &stack0xffffffc4;
              *(short *)(&stack0xffffffc4 + param_3 * 2) = -1;
              local_20[param_3 + -0xf] = 0xffff;
              BVar2 = GetStringTypeA(param_6,param_1,&stack0xffffffc4,_Size,(LPWORD)&stack0xffffffc4
                                    );
              if ((local_20[param_3 + -0xf] != 0xffff) &&
                 (*(short *)(&stack0xffffffc4 + param_3 * 2) == -1)) {
                FUN__text1__008487d0(param_4,&stack0xffffffc4,param_3 * 2);
                ExceptionList = local_14;
                return BVar2;
              }
            }
          }
        }
      }
    }
    ExceptionList = local_14;
    return 0;
  }
  BVar2 = GetStringTypeW(param_1,param_2,param_3,param_4);
  ExceptionList = local_14;
  return BVar2;
}

