
undefined4 FUN__text__0052afe6(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 uVar2;
  undefined1 local_40 [60];
  
  iVar1 = (*API_GDI32_DLL_GetObjectA)(param_2,0x3c,local_40);
  if (iVar1 == 0) {
    uVar2 = 0x8876086c;
  }
  else {
    uVar2 = FUN__text__0052ae11(param_1,local_40,param_3);
  }
  return uVar2;
}

