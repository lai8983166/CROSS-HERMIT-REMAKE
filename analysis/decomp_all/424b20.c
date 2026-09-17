
void FUN__text__00424b20(undefined4 param_1,int param_2,undefined4 param_3,int *param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [12];
  undefined4 uStack_20;
  undefined4 local_10;
  int *local_c;
  int *local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_GetPropA)(param_1,"CPP_CLASS");
  local_8 = (int *)FUN__text__0056ce80();
  if (local_8 == (int *)0x0) {
    if ((param_2 == 1) || (param_2 == 0x81)) {
      local_c = param_4;
      local_8 = (int *)*param_4;
    }
    else if (param_2 == 0x110) {
      local_8 = param_4;
    }
    if (local_8 != (int *)0x0) {
      FUN__text__00424730(param_1,1);
    }
  }
  if (local_8 == (int *)0x0) {
    (*API_USER32_DLL_GetWindowLongA)(param_1,4);
    iVar1 = FUN__text__0056ce80();
    if (iVar1 == 0) {
      (*API_USER32_DLL_DefFrameProcA)(param_1,0,param_2,param_3,param_4);
      FUN__text__0056ce80();
    }
  }
  else {
    (**(code **)(*local_8 + 4))(param_1,param_2,param_3,param_4);
    local_10 = FUN__text__0056ce80();
    if (param_2 == 2) {
      FUN__text__004248e0();
    }
  }
  uStack_20 = 0x424c26;
  FUN__text__0056ce80();
  return;
}

