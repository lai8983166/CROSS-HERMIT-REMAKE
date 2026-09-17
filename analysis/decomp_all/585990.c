
bool FUN__text__00585990(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  
  iVar1 = (*API_KERNEL32_DLL_IsBadReadPtr)(param_1,param_2);
  return iVar1 == 0;
}

