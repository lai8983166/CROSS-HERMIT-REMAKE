
/* Library Function - Single Match
    int __cdecl _ValidateExecute(int (__stdcall*)(void))
   
   Libraries: Visual Studio 2003 Debug, Visual Studio 2003 Release */

int __cdecl _ValidateExecute(_func_int *param_1)

{
  int iVar1;
  uint local_8;
  
  iVar1 = (*API_KERNEL32_DLL_IsBadCodePtr)(param_1);
  local_8 = (uint)(iVar1 == 0);
  return local_8;
}

