
undefined4 FUN__text__0058e390(char *param_1,int param_2)

{
  char *pcVar1;
  int iVar2;
  int *piVar3;
  size_t sVar4;
  bool bVar5;
  undefined4 uVar6;
  char *pcVar7;
  undefined4 uVar8;
  int local_c;
  
  if (((param_1 == (char *)0x0) ||
      (pcVar1 = (char *)FUN__text__0058e7e0(param_1,0x3d), pcVar1 == (char *)0x0)) ||
     (param_1 == pcVar1)) {
    return 0xffffffff;
  }
  bVar5 = pcVar1[1] == '\0';
  if (DAT_0080a408 == DAT_0080a40c) {
    DAT_0080a408 = (int *)copy_environ(DAT_0080a408);
  }
  if (DAT_0080a408 == (int *)0x0) {
    if ((param_2 == 0) || (DAT_0080a410 == (undefined4 *)0x0)) {
      if (bVar5) {
        return 0;
      }
      DAT_0080a408 = (int *)__malloc_dbg(4,2,"setenv.c",0x87);
      if (DAT_0080a408 == (int *)0x0) {
        return 0xffffffff;
      }
      *DAT_0080a408 = 0;
      if (DAT_0080a410 == (undefined4 *)0x0) {
        DAT_0080a410 = (undefined4 *)__malloc_dbg(4,2,"setenv.c",0x8e);
        if (DAT_0080a410 == (undefined4 *)0x0) {
          return 0xffffffff;
        }
        *DAT_0080a410 = 0;
      }
    }
    else {
      iVar2 = FUN__text__0058de90();
      if (iVar2 != 0) {
        return 0xffffffff;
      }
    }
  }
  piVar3 = DAT_0080a408;
  local_c = findenv(param_1,(int)pcVar1 - (int)param_1);
  if ((local_c < 0) || (*piVar3 == 0)) {
    if (bVar5) {
      return 0;
    }
    if (local_c < 0) {
      local_c = -local_c;
    }
    piVar3 = (int *)FID_conflict___realloc_dbg(piVar3,local_c * 4 + 8,2,"setenv.c",0xce);
    if (piVar3 == (int *)0x0) {
      return 0xffffffff;
    }
    piVar3[local_c] = (int)param_1;
    piVar3[local_c + 1] = 0;
    DAT_0080a408 = piVar3;
  }
  else if (bVar5) {
    __free_dbg(piVar3[local_c],2);
    for (; piVar3[local_c] != 0; local_c = local_c + 1) {
      piVar3[local_c] = piVar3[local_c + 1];
    }
    piVar3 = (int *)FID_conflict___realloc_dbg(piVar3,local_c << 2,2,"setenv.c",0xb9);
    if (piVar3 != (int *)0x0) {
      DAT_0080a408 = piVar3;
    }
  }
  else {
    piVar3[local_c] = (int)param_1;
  }
  if (param_2 != 0) {
    uVar8 = 0xe5;
    pcVar7 = "setenv.c";
    uVar6 = 2;
    sVar4 = _strlen(param_1);
    iVar2 = __malloc_dbg(sVar4 + 2,uVar6,pcVar7,uVar8);
    if (iVar2 != 0) {
      FUN__text__0056cd90(iVar2,param_1);
      pcVar1[iVar2 - (int)param_1] = '\0';
      (*DAT_005921c8)(iVar2,~-(uint)bVar5 & (uint)(pcVar1 + (iVar2 - (int)param_1) + 1));
      __free_dbg(iVar2,2);
    }
  }
  return 0;
}

