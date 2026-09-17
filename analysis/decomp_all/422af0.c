
void FUN__text__00422af0(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_80 [16];
  undefined1 local_40 [8];
  undefined4 local_38;
  undefined4 local_34;
  int local_30;
  int local_2c;
  undefined1 local_28 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_80;
  for (iVar1 = 0x1f; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_SetWindowRgn)(param_1,0,1);
  local_30 = FUN__text__0056ce80();
  if (local_30 != 0) {
    if (*local_8 != 0) {
      (*API_GDI32_DLL_DeleteObject)(*local_8);
      FUN__text__0056ce80();
      *local_8 = 0;
    }
    (*API_USER32_DLL_GetWindowRect)(param_1,&local_18);
    FUN__text__0056ce80();
    (*API_USER32_DLL_GetClientRect)(param_1,local_28);
    FUN__text__0056ce80();
    local_10 = local_10 - local_18;
    local_c = local_c - local_14;
    local_18 = 0;
    local_14 = 0;
    (*API_USER32_DLL_GetSystemMetrics)(0x37);
    iVar1 = FUN__text__0056ce80();
    (*API_USER32_DLL_GetSystemMetrics)(4);
    local_2c = FUN__text__0056ce80();
    local_2c = iVar1 + local_2c;
    (*API_USER32_DLL_GetClientRect)(param_1,local_40);
    FUN__text__0056ce80();
    iVar1 = FUN__text__00422f20(param_2,local_38,local_34,param_3);
    *local_8 = iVar1;
    if (*local_8 != 0) {
      (*API_USER32_DLL_SetWindowRgn)(param_1,*local_8,1);
      local_30 = FUN__text__0056ce80();
    }
  }
  local_14 = 0x422c51;
  FUN__text__0056ce80();
  return;
}

