
/* Library Function - Single Match
    __isatty
   
   Library: Visual Studio 2003 Debug */

int __cdecl __isatty(int _FileHandle)

{
  uint uVar1;
  
  if ((uint)_FileHandle < DAT_0080a900) {
    uVar1 = (int)*(char *)((&DAT_0080a800)[_FileHandle >> 5] + 4 + (_FileHandle & 0x1fU) * 0x24) &
            0x40;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

