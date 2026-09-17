
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text1__0084c6d3(void)

{
  char cVar1;
  char cVar2;
  char *_Str1;
  DWORD DVar3;
  int iVar4;
  size_t sVar5;
  char *_Source;
  int local_4;
  
  DAT_008757e8 = 0;
  DAT_00872918 = 0xffffffff;
  DAT_00872908 = 0xffffffff;
  _Str1 = (char *)FUN__text1__0084d6b4(&DAT_0087437c);
  if (_Str1 == (char *)0x0) {
    DVar3 = GetTimeZoneInformation((LPTIME_ZONE_INFORMATION)&DAT_008757f0);
    if (DVar3 == 0xffffffff) {
      return;
    }
    DAT_00872870 = DAT_008757f0 * 0x3c;
    DAT_008757e8 = 1;
    if (DAT_00875836 != 0) {
      DAT_00872870 = DAT_00872870 + DAT_00875844 * 0x3c;
    }
    if ((DAT_0087588a == 0) || (DAT_00875898 == 0)) {
      DAT_00872874 = 0;
      _DAT_00872878 = 0;
    }
    else {
      DAT_00872874 = 1;
      _DAT_00872878 = (DAT_00875898 - DAT_00875844) * 0x3c;
    }
    iVar4 = WideCharToMultiByte(DAT_008758cc,0x220,L"",-1,PTR_DAT_008728fc,0x3f,(LPCSTR)0x0,&local_4
                               );
    if ((iVar4 == 0) || (local_4 != 0)) {
      *PTR_DAT_008728fc = 0;
    }
    else {
      PTR_DAT_008728fc[0x3f] = 0;
    }
    iVar4 = WideCharToMultiByte(DAT_008758cc,0x220,L"",-1,PTR_DAT_00872900,0x3f,(LPCSTR)0x0,&local_4
                               );
    if ((iVar4 != 0) && (local_4 == 0)) {
      PTR_DAT_00872900[0x3f] = 0;
      return;
    }
  }
  else {
    if (*_Str1 == '\0') {
      return;
    }
    if ((DAT_0087589c != (char *)0x0) && (iVar4 = _strcmp(_Str1,DAT_0087589c), iVar4 == 0)) {
      return;
    }
    FUN__text1__008497d3(DAT_0087589c);
    sVar5 = _strlen(_Str1);
    DAT_0087589c = _malloc(sVar5 + 1);
    if (DAT_0087589c == (char *)0x0) {
      return;
    }
    FUN__text1__00848d20(DAT_0087589c,_Str1);
    _strncpy(PTR_DAT_008728fc,_Str1,3);
    _Source = _Str1 + 3;
    PTR_DAT_008728fc[3] = 0;
    cVar1 = *_Source;
    if (cVar1 == '-') {
      _Source = _Str1 + 4;
    }
    iVar4 = FUN__text1__008493f8(_Source);
    DAT_00872870 = iVar4 * 0xe10;
    for (; (cVar2 = *_Source, cVar2 == '+' || (('/' < cVar2 && (cVar2 < ':'))));
        _Source = _Source + 1) {
    }
    if (*_Source == ':') {
      _Source = _Source + 1;
      iVar4 = FUN__text1__008493f8(_Source);
      DAT_00872870 = DAT_00872870 + iVar4 * 0x3c;
      for (; ('/' < *_Source && (*_Source < ':')); _Source = _Source + 1) {
      }
      if (*_Source == ':') {
        _Source = _Source + 1;
        iVar4 = FUN__text1__008493f8(_Source);
        DAT_00872870 = DAT_00872870 + iVar4;
        for (; ('/' < *_Source && (*_Source < ':')); _Source = _Source + 1) {
        }
      }
    }
    if (cVar1 == '-') {
      DAT_00872870 = -DAT_00872870;
    }
    DAT_00872874 = (int)*_Source;
    if (DAT_00872874 != 0) {
      _strncpy(PTR_DAT_00872900,_Source,3);
      PTR_DAT_00872900[3] = 0;
      return;
    }
  }
  *PTR_DAT_00872900 = 0;
  return;
}

