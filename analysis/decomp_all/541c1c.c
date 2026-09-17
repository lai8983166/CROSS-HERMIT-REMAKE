
/* WARNING: Type propagation algorithm not settling */

int FUN__text__00541c1c(void)

{
  int iVar1;
  int local_14;
  int local_10 [3];
  
  iVar1 = (*API_ADVAPI32_DLL_RegOpenKeyA)(0x80000002,"Software\\Microsoft\\Direct3D",local_10 + 2);
  if (iVar1 == 0) {
    local_10[1] = 4;
    iVar1 = (*API_ADVAPI32_DLL_RegQueryValueExA)
                      (local_10[2],"DisableMMX",0,local_10,&local_14,local_10 + 1);
    if (((iVar1 == 0) && (local_10[0] == 4)) && (local_14 != 0)) {
      (*API_ADVAPI32_DLL_RegCloseKey)(local_10[2]);
      DAT_0075ed90 = 0;
      return 0;
    }
    (*API_ADVAPI32_DLL_RegCloseKey)(local_10[2]);
  }
  if (DAT_0075ed90 < 0) {
    DAT_0075ed90 = 0;
    iVar1 = FUN__text__00541bf7();
    if (iVar1 != 0) {
      DAT_0075ed90 = 1;
    }
  }
  return DAT_0075ed90;
}

