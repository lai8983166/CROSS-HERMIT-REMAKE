
undefined4 FUN__text__00541b9b(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  int local_c;
  undefined4 local_8;
  
  local_8 = 0;
  iVar1 = (*API_ADVAPI32_DLL_RegOpenKeyA)(0x80000002,"Software\\Microsoft\\Direct3D",&local_8);
  if (iVar1 == 0) {
    iVar1 = (*API_ADVAPI32_DLL_RegQueryValueExA)
                      (local_8,param_2,0,&local_c,param_3,&stack0x00000010);
    (*API_ADVAPI32_DLL_RegCloseKey)(local_8);
    if ((iVar1 == 0) && (local_c == param_1)) {
      return 1;
    }
  }
  return 0;
}

