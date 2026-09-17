
/* Library Function - Single Match
    __callnewh
   
   Library: Visual Studio 2003 Debug */

int __cdecl __callnewh(size_t _Size)

{
  int iVar1;
  
  if ((DAT_0080a4f0 != (code *)0x0) && (iVar1 = (*DAT_0080a4f0)(_Size), iVar1 != 0)) {
    return 1;
  }
  return 0;
}

