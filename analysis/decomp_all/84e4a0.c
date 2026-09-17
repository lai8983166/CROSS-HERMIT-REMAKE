
/* Library Function - Single Match
    __strcmpi
   
   Libraries: Visual Studio 1998 Debug, Visual Studio 1998 Release */

int __cdecl __strcmpi(char *_Str1,char *_Str2)

{
  char cVar1;
  uint uVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  char cVar6;
  int iVar7;
  
  if (DAT_008758bc == 0) {
    bVar5 = 0xff;
    do {
      do {
        cVar6 = '\0';
        if (bVar5 == 0) goto LAB__text1__0084e4ee;
        bVar5 = *_Str2;
        _Str2 = _Str2 + 1;
        bVar4 = *_Str1;
        _Str1 = _Str1 + 1;
      } while (bVar4 == bVar5);
      bVar3 = bVar5 + 0xbf + (-((byte)(bVar5 + 0xbf) < 0x1a) & 0x20U) + 0x41;
      bVar4 = bVar4 + 0xbf;
      bVar5 = bVar4 + (-(bVar4 < 0x1a) & 0x20U) + 0x41;
    } while (bVar5 == bVar3);
    cVar6 = (bVar5 < bVar3) * -2 + '\x01';
LAB__text1__0084e4ee:
    iVar7 = (int)cVar6;
  }
  else {
    iVar7 = 0xff;
    do {
      do {
        if ((char)iVar7 == '\0') {
          return iVar7;
        }
        cVar6 = *_Str2;
        iVar7 = CONCAT31((int3)((uint)iVar7 >> 8),cVar6);
        _Str2 = _Str2 + 1;
        cVar1 = *_Str1;
        _Str1 = _Str1 + 1;
      } while (cVar6 == cVar1);
      bVar5 = FUN__text1__0084e65d(cVar1,iVar7);
      iVar7 = FUN__text1__0084e65d();
    } while (bVar5 == (byte)iVar7);
    uVar2 = (uint)(bVar5 < (byte)iVar7);
    iVar7 = (1 - uVar2) - (uint)(uVar2 != 0);
  }
  return iVar7;
}

