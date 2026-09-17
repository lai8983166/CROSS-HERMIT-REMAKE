
/* Library Function - Single Match
    _rand
   
   Libraries: Visual Studio 2003 Debug, Visual Studio 2005 Debug, Visual Studio 2008 Debug */

int __cdecl _rand(void)

{
  int iVar1;
  
  iVar1 = FUN__text__005753b0();
  *(int *)(iVar1 + 0x14) = *(int *)(iVar1 + 0x14) * 0x343fd + 0x269ec3;
  return *(uint *)(iVar1 + 0x14) >> 0x10 & 0x7fff;
}

