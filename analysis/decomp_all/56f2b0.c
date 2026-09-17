
/* Library Function - Multiple Matches With Different Base Names
    __expand
    _realloc
   
   Library: Visual Studio 2003 Debug */

void * __cdecl FID_conflict___expand(void *_Memory,size_t _NewSize)

{
  void *pvVar1;
  
  pvVar1 = (void *)FID_conflict___realloc_dbg(_Memory,_NewSize,1,0,0);
  return pvVar1;
}

