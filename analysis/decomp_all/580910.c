
/* Library Function - Single Match
    __whiteout
   
   Library: Visual Studio 2003 Debug */

undefined4 __thiscall __whiteout(undefined4 param_1,int *param_2,undefined4 param_3)

{
  int iVar1;
  
  do {
    *param_2 = *param_2 + 1;
    param_1 = __inc(param_3,param_1);
    iVar1 = FUN__text__00571910(param_1);
  } while (iVar1 != 0);
  return param_1;
}

