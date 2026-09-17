
/* Library Function - Single Match
    __endthreadex
   
   Library: Visual Studio 2003 Debug */

void __cdecl __endthreadex(uint _Retval)

{
  int iVar1;
  
  if (PTR_DAT_00761980 != (undefined *)0x0) {
    (*(code *)PTR_DAT_00761980)();
  }
  iVar1 = FUN__text__005753b0();
  if (iVar1 == 0) {
    __amsg_exit(0x10);
  }
  FUN__text__00575450(iVar1);
  (*DAT_005921a4)(_Retval);
  return;
}

