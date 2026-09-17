
void FUN__text__0056d070(undefined4 param_1,int param_2)

{
  void *pvVar1;
  
  pvVar1 = ExceptionList;
  FUN__text__0058e93c(param_1,0x56d09c,param_2,0);
  *(uint *)(param_2 + 4) = *(uint *)(param_2 + 4) & 0xfffffffd;
  *(void **)pvVar1 = ExceptionList;
  ExceptionList = pvVar1;
  return;
}

