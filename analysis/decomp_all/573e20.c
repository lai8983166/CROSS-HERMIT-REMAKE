
/* Library Function - Single Match
    __setdefaultprecision
   
   Library: Visual Studio 2003 Debug */

void __setdefaultprecision(void)

{
  __controlfp(0x10000,0x30000);
  return;
}

