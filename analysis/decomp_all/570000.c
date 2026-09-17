
/* Library Function - Multiple Matches With Different Base Names
    int __cdecl ATL::AtlIsValidAddress(void const *,unsigned int,int)
    __CrtIsValidPointer
   
   Library: Visual Studio 2003 Debug */

int __cdecl ATL::AtlIsValidAddress(void *param_1,uint param_2,int param_3)

{
  int iVar1;
  
  if (((param_1 != (void *)0x0) &&
      (iVar1 = (*API_KERNEL32_DLL_IsBadReadPtr)(param_1,param_2), iVar1 == 0)) &&
     ((param_3 == 0 || (iVar1 = (*API_KERNEL32_DLL_IsBadWritePtr)(param_1,param_2), iVar1 == 0)))) {
    return 1;
  }
  return 0;
}

