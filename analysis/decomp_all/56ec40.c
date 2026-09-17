
/* Library Function - Single Match
    _calloc
   
   Library: Visual Studio 2003 Debug */

void * __cdecl _calloc(size_t _Count,size_t _Size)

{
  void *pvVar1;
  
  pvVar1 = (void *)__calloc_dbg(_Count,_Size,1,0,0);
  return pvVar1;
}

