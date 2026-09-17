
/* Library Function - Single Match
    __FF_MSGBANNER
   
   Library: Visual Studio 2003 Debug */

void __cdecl __FF_MSGBANNER(void)

{
  if ((DAT_0080a468 == 1) || ((DAT_0080a468 == 0 && (DAT_007619fc == 1)))) {
    FUN_0057d9d0(0xfc);
    if (DAT_0080a604 != (code *)0x0) {
      (*DAT_0080a604)();
    }
    FUN_0057d9d0(0xff);
  }
  return;
}

