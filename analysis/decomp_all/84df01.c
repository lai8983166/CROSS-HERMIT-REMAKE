
undefined4 FUN__text1__0084df01(char *param_1,int param_2)

{
  char *pcVar1;
  int iVar2;
  int *piVar3;
  size_t sVar4;
  LPCSTR lpName;
  int *piVar5;
  bool bVar6;
  
  if (param_1 == (char *)0x0) {
    return 0xffffffff;
  }
  pcVar1 = (char *)FUN__text1__0084e3e7(param_1,0x3d);
  if (pcVar1 == (char *)0x0) {
    return 0xffffffff;
  }
  if (param_1 == pcVar1) {
    return 0xffffffff;
  }
  bVar6 = pcVar1[1] == '\0';
  if (DAT_00875674 == DAT_00875678) {
    DAT_00875674 = (int *)FUN__text1__0084e0e0(DAT_00875674);
  }
  if (DAT_00875674 == (int *)0x0) {
    if ((param_2 == 0) || (DAT_0087567c == (undefined4 *)0x0)) {
      if (bVar6) {
        return 0;
      }
      DAT_00875674 = _malloc(4);
      if (DAT_00875674 == (int *)0x0) {
        return 0xffffffff;
      }
      *DAT_00875674 = 0;
      if (DAT_0087567c == (undefined4 *)0x0) {
        DAT_0087567c = _malloc(4);
        if (DAT_0087567c == (undefined4 *)0x0) {
          return 0xffffffff;
        }
        *DAT_0087567c = 0;
      }
    }
    else {
      iVar2 = FUN__text1__0084db38();
      if (iVar2 != 0) {
        return 0xffffffff;
      }
    }
  }
  piVar3 = DAT_00875674;
  iVar2 = FUN__text1__0084e088(param_1,(int)pcVar1 - (int)param_1);
  if ((iVar2 < 0) || (*piVar3 == 0)) {
    if (bVar6) {
      return 0;
    }
    if (iVar2 < 0) {
      iVar2 = -iVar2;
    }
    piVar3 = (int *)FUN__text1__0084e147(piVar3,iVar2 * 4 + 8);
    if (piVar3 == (int *)0x0) {
      return 0xffffffff;
    }
    piVar3[iVar2] = (int)param_1;
    piVar3[iVar2 + 1] = 0;
  }
  else {
    if (!bVar6) {
      piVar3[iVar2] = (int)param_1;
      goto LAB__text1__0084e035;
    }
    piVar5 = piVar3 + iVar2;
    FUN__text1__008497d3(piVar3[iVar2]);
    for (; *piVar5 != 0; piVar5 = piVar5 + 1) {
      iVar2 = iVar2 + 1;
      *piVar5 = piVar5[1];
    }
    piVar3 = (int *)FUN__text1__0084e147(piVar3,iVar2 << 2);
    if (piVar3 == (int *)0x0) goto LAB__text1__0084e035;
  }
  DAT_00875674 = piVar3;
LAB__text1__0084e035:
  if (param_2 != 0) {
    sVar4 = _strlen(param_1);
    lpName = _malloc(sVar4 + 2);
    if (lpName != (LPCSTR)0x0) {
      FUN__text1__00848d20(lpName,param_1);
      pcVar1[(int)lpName - (int)param_1] = '\0';
      SetEnvironmentVariableA
                (lpName,(LPCSTR)(~-(uint)bVar6 & (uint)(pcVar1 + ((int)lpName - (int)param_1) + 1)))
      ;
      FUN__text1__008497d3(lpName);
    }
  }
  return 0;
}

