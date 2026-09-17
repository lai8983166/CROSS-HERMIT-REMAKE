
/* Library Function - Single Match
    __nh_malloc_base
   
   Library: Visual Studio 2003 Debug */

int __thiscall __nh_malloc_base(int param_1,uint param_2,int param_3)

{
  int iVar1;
  
  if (param_2 < 0xffffffe1) {
    do {
      if (param_2 < 0xffffffe1) {
        param_1 = __heap_alloc_base(param_2,param_1);
      }
      else {
        param_1 = 0;
      }
      if (param_1 != 0) {
        return param_1;
      }
      if (param_3 == 0) {
        return 0;
      }
      iVar1 = __callnewh(param_2);
    } while (iVar1 != 0);
  }
  return 0;
}

