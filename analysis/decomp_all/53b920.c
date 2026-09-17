
undefined4 __thiscall
FUN__text__0053b920(int *param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5)

{
  int iVar1;
  int iVar2;
  code *pcVar3;
  
  if (*param_1 != 0) {
    FUN__text__0053b901();
  }
  pcVar3 = DAT_0059225c;
  if (param_5 == 0) {
    pcVar3 = DAT_00592298;
  }
  if (((param_4 != 0) && (iVar1 = (*pcVar3)(param_2,param_3,2), iVar1 != 0)) ||
     (iVar1 = (*pcVar3)(param_2,param_3,10), iVar1 != 0)) {
    iVar2 = (*API_KERNEL32_DLL_SizeofResource)(param_2,iVar1);
    param_1[2] = iVar2;
    if (iVar2 != 0) {
      iVar1 = (*API_KERNEL32_DLL_LoadResource)(param_2,iVar1);
      *param_1 = iVar1;
      if (iVar1 != 0) {
        iVar1 = (*DAT_00592118)(iVar1);
        param_1[1] = iVar1;
        if (iVar1 != 0) {
          return 0;
        }
      }
    }
  }
  (*API_KERNEL32_DLL_GetLastError)();
  return 0x88760b59;
}

