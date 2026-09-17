
void * FUN__text__0054bc20(int param_1,size_t param_2)

{
  void *pvVar1;
  
  if ((param_1 != 0) && (param_2 != 0)) {
    pvVar1 = _malloc(param_2);
    if (pvVar1 == (void *)0x0) {
      FUN__text__0054381d(param_1,"Out of Memory");
    }
    return pvVar1;
  }
  return (void *)0x0;
}

