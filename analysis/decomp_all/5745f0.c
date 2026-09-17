
/* Library Function - Single Match
    __shift
   
   Library: Visual Studio */

void __shift(char *param_1,int param_2)

{
  size_t sVar1;
  
  if (param_2 != 0) {
    sVar1 = _strlen(param_1);
    FUN__text__005855a0(param_1 + param_2,param_1,sVar1 + 1);
  }
  return;
}

