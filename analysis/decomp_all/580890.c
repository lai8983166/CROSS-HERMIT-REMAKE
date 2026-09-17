
/* Library Function - Single Match
    __inc
   
   Library: Visual Studio 2003 Debug */

uint __thiscall __inc(undefined4 param_1,int *param_2)

{
  uint uVar1;
  
  param_2[1] = param_2[1] + -1;
  if (param_2[1] < 0) {
    uVar1 = FUN__text__00589220(param_2,param_1);
  }
  else {
    uVar1 = (uint)*(byte *)*param_2;
    *param_2 = *param_2 + 1;
  }
  return uVar1;
}

