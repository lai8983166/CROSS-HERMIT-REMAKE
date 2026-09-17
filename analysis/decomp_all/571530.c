
/* Library Function - Single Match
    __amsg_exit
   
   Library: Visual Studio 2003 Debug */

void __cdecl __amsg_exit(int param_1)

{
  if (DAT_0080a468 == 1) {
    __FF_MSGBANNER();
  }
  FUN_0057d9d0(param_1);
  (*(code *)PTR___exit_007619f8)(0xff);
  return;
}

