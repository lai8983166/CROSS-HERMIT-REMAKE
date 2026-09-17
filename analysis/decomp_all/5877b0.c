
void FUN__text__005877b0(void)

{
  char *_Str1;
  int iVar1;
  size_t sVar2;
  undefined4 uVar3;
  char *pcVar4;
  undefined4 uVar5;
  char *local_10;
  int local_c;
  int local_8;
  
  local_8 = 0;
  FUN__text__00577040(0xc);
  DAT_0080a6c0 = 0;
  DAT_00764f78 = 0xffffffff;
  DAT_00764f68 = 0xffffffff;
  _Str1 = FID_conflict___getenv_lk("TZ");
  if (_Str1 == (char *)0x0) {
    FUN__text__005770e0(0xc);
    iVar1 = (*API_KERNEL32_DLL_GetTimeZoneInformation)(&DAT_0080a6c8);
    if (iVar1 != -1) {
      DAT_0080a6c0 = 1;
      DAT_00764ed0 = DAT_0080a6c8 * 0x3c;
      if (DAT_0080a70e != 0) {
        DAT_00764ed0 = DAT_00764ed0 + DAT_0080a71c * 0x3c;
      }
      if ((DAT_0080a762 == 0) || (DAT_0080a770 == 0)) {
        DAT_00764ed4 = 0;
        DAT_00764ed8 = 0;
      }
      else {
        DAT_00764ed4 = 1;
        DAT_00764ed8 = (DAT_0080a770 - DAT_0080a71c) * 0x3c;
      }
      iVar1 = (*API_KERNEL32_DLL_WideCharToMultiByte)
                        (DAT_0080a63c,0x220,&DAT_0080a6cc,0xffffffff,PTR_DAT_00764f5c,0x3f,0,
                         &local_c);
      if ((iVar1 == 0) || (local_c != 0)) {
        *PTR_DAT_00764f5c = 0;
      }
      else {
        PTR_DAT_00764f5c[0x3f] = 0;
      }
      iVar1 = (*API_KERNEL32_DLL_WideCharToMultiByte)
                        (DAT_0080a63c,0x220,&DAT_0080a720,0xffffffff,PTR_DAT_00764f60,0x3f,0,
                         &local_c);
      if ((iVar1 == 0) || (local_c != 0)) {
        *PTR_DAT_00764f60 = 0;
      }
      else {
        PTR_DAT_00764f60[0x3f] = 0;
      }
    }
  }
  else if ((*_Str1 == '\0') ||
          ((DAT_0080a774 != (char *)0x0 && (iVar1 = _strcmp(_Str1,DAT_0080a774), iVar1 == 0)))) {
    FUN__text__005770e0(0xc);
  }
  else {
    __free_dbg(DAT_0080a774,2);
    uVar5 = 0x10c;
    pcVar4 = "tzset.c";
    uVar3 = 2;
    sVar2 = _strlen(_Str1);
    DAT_0080a774 = (char *)__malloc_dbg(sVar2 + 1,uVar3,pcVar4,uVar5);
    if (DAT_0080a774 == (char *)0x0) {
      FUN__text__005770e0(0xc);
    }
    else {
      FUN__text__0056cd90(DAT_0080a774,_Str1);
      FUN__text__005770e0(0xc);
      _strncpy(PTR_DAT_00764f5c,_Str1,3);
      PTR_DAT_00764f5c[3] = 0;
      local_10 = _Str1 + 3;
      if (*local_10 == '-') {
        local_8 = local_8 + 1;
        local_10 = _Str1 + 4;
      }
      iVar1 = FUN__text__00572740(local_10);
      DAT_00764ed0 = iVar1 * 0xe10;
      for (; (*local_10 == '+' || (('/' < *local_10 && (*local_10 < ':')))); local_10 = local_10 + 1
          ) {
      }
      if (*local_10 == ':') {
        local_10 = local_10 + 1;
        iVar1 = FUN__text__00572740(local_10);
        DAT_00764ed0 = DAT_00764ed0 + iVar1 * 0x3c;
        for (; ('/' < *local_10 && (*local_10 < ':')); local_10 = local_10 + 1) {
        }
        if (*local_10 == ':') {
          local_10 = local_10 + 1;
          iVar1 = FUN__text__00572740(local_10);
          DAT_00764ed0 = DAT_00764ed0 + iVar1;
          for (; ('/' < *local_10 && (*local_10 < ':')); local_10 = local_10 + 1) {
          }
        }
      }
      if (local_8 != 0) {
        DAT_00764ed0 = -DAT_00764ed0;
      }
      DAT_00764ed4 = (int)*local_10;
      if (DAT_00764ed4 == 0) {
        *PTR_DAT_00764f60 = 0;
      }
      else {
        _strncpy(PTR_DAT_00764f60,local_10,3);
        PTR_DAT_00764f60[3] = 0;
      }
    }
  }
  return;
}

