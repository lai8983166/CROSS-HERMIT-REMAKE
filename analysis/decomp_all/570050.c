
undefined4 FUN_00570050(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined1 local_14 [4];
  char *local_10;
  undefined1 local_c [4];
  int local_8;
  
  if (param_1 == 0) {
    uVar1 = 0;
  }
  else {
    iVar2 = ATL::AtlIsValidAddress((void *)(param_1 + -0x20),0x20,1);
    if (iVar2 == 0) {
      uVar1 = 0;
    }
    else if (DAT_0080ab2c == 3) {
      local_8 = FUN_00578c00(param_1 + -0x20);
      if (local_8 == 0) {
        if ((DAT_0080a3ec & 0x8000) == 0) {
          uVar1 = (*API_KERNEL32_DLL_HeapValidate)(DAT_0080ab28,0,param_1 + -0x20);
        }
        else {
          uVar1 = 1;
        }
      }
      else {
        uVar1 = FUN_00578c60(local_8,param_1 + -0x20);
      }
    }
    else if (DAT_0080ab2c == 2) {
      local_10 = (char *)FUN_0057ac20(param_1 + -0x20,local_14,local_c);
      if (local_10 == (char *)0x0) {
        if ((DAT_0080a3ec & 0x8000) == 0) {
          uVar1 = (*API_KERNEL32_DLL_HeapValidate)(DAT_0080ab28,0,param_1 + -0x20);
        }
        else {
          uVar1 = 1;
        }
      }
      else if (*local_10 == '\0') {
        uVar1 = 0;
      }
      else {
        uVar1 = 1;
      }
    }
    else {
      uVar1 = (*API_KERNEL32_DLL_HeapValidate)(DAT_0080ab28,0,param_1 + -0x20);
    }
  }
  return uVar1;
}

