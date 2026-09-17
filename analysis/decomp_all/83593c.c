
undefined4 FUN__text1__0083593c(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  char *_Str;
  size_t sVar4;
  CHAR local_10c [256];
  code *local_c;
  int local_8;
  
  SetEnvironmentVariableA("INITIALIZEDLLADDR",(LPCSTR)0x0);
  pcVar1 = DAT_008750c8;
  if (DAT_008750c8 != (code *)0x0) {
    local_c = DAT_008750c8;
    DAT_008750c8 = (code *)0x0;
    iVar2 = (*pcVar1)();
    if (iVar2 == 0) {
      return 0;
    }
  }
  local_8 = FUN__text1__0083586e();
  if (local_8 == 1) {
    if (DAT_00874eb8 == (code *)0x0) {
      uVar3 = 1;
    }
    else {
      local_8 = (*DAT_00874eb8)(PTR_IMAGE_DOS_HEADER_008751e8,1,&DAT_008750dc);
      if (local_8 == 0) {
        FUN__text1__00835914();
        uVar3 = 0;
      }
      else {
        uVar3 = 1;
      }
    }
  }
  else if (local_8 == 0) {
    uVar3 = FUN__text1__00833f91();
    FUN__text1__00848d20(local_10c,uVar3);
    _Str = (char *)FUN__text1__00833fa2();
    sVar4 = _strlen(_Str);
    if (sVar4 != 0) {
      FUN__text1__00848d30(local_10c,&DAT_0086e6dc);
      uVar3 = FUN__text1__00833fa2();
      FUN__text1__00848d30(local_10c,uVar3);
    }
    MessageBoxA((HWND)0x0,local_10c,(LPCSTR)0x0,0x40010);
    uVar3 = 0;
  }
  else {
    uVar3 = 0;
  }
  return uVar3;
}

