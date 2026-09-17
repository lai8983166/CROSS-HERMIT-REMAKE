
/* Library Function - Single Match
    ___sbh_heap_init
   
   Libraries: Visual Studio 2003 Debug, Visual Studio 2005 Debug, Visual Studio 2008 Debug */

bool ___sbh_heap_init(undefined4 param_1)

{
  DAT_0080ab48 = (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,0x140);
  if (DAT_0080ab48 != 0) {
    DAT_0080ab4c = param_1;
    DAT_0080ab40 = 0;
    DAT_0080ab44 = 0;
    DAT_0080ab30 = 0x10;
    DAT_0080ab38 = DAT_0080ab48;
  }
  return DAT_0080ab48 != 0;
}

