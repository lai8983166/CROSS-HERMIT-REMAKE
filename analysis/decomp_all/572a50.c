
/* Library Function - Single Match
    __strdup
   
   Library: Visual Studio 2003 Debug */

char * __cdecl __strdup(char *_Src)

{
  char *pcVar1;
  size_t sVar2;
  void *pvVar3;
  
  if (_Src == (char *)0x0) {
    pcVar1 = (char *)0x0;
  }
  else {
    sVar2 = _strlen(_Src);
    pvVar3 = _malloc(sVar2 + 1);
    if (pvVar3 == (void *)0x0) {
      pcVar1 = (char *)0x0;
    }
    else {
      pcVar1 = (char *)FUN__text__0056cd90(pvVar3,_Src);
    }
  }
  return pcVar1;
}

