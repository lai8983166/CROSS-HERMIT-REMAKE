
/* Library Function - Single Match
    _setSBCS
   
   Library: Visual Studio 2003 Debug */

void __cdecl setSBCS(void)

{
  int local_8;
  
  for (local_8 = 0; local_8 < 0x101; local_8 = local_8 + 1) {
    (&DAT_0080aa20)[local_8] = 0;
  }
  DAT_0080a904 = 0;
  DAT_0080a91c = 0;
  DAT_0080ab24 = 0;
  for (local_8 = 0; local_8 < 6; local_8 = local_8 + 1) {
    *(undefined2 *)(&DAT_0080a910 + local_8 * 2) = 0;
  }
  return;
}

