
/* Library Function - Single Match
    _write_multi_char
   
   Libraries: Visual Studio 2003 Debug, Visual Studio 2005 Debug */

void __cdecl write_multi_char(undefined2 param_1,int param_2,undefined4 param_3,int *param_4)

{
  do {
    if (param_2 < 1) {
      return;
    }
    FUN__text__00583a00(CONCAT22((short)((uint)(param_2 + -1) >> 0x10),param_1),param_3,param_4);
    param_2 = param_2 + -1;
  } while (*param_4 != -1);
  return;
}

