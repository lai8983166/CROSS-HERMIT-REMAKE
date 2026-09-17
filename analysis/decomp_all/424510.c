
void FUN__text__00424510(int *param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  if (param_4 == -1) {
    param_4 = *param_1;
  }
  (*API_GDI32_DLL_CreateRectRgn)(0,0,0,0);
  local_c = FUN__text__0056ce80();
  local_18 = 0;
  do {
    if (param_3 <= local_18) {
      local_18 = 0x42465d;
      FUN__text__0056ce80();
      return;
    }
    for (local_1c = 0; iVar1 = local_1c, local_1c < param_2; local_1c = local_1c + 1) {
      if (*param_1 != param_4) {
        local_14 = local_1c;
        do {
          local_1c = local_1c + 1;
          if (param_2 <= local_1c) break;
          param_1 = param_1 + 1;
        } while (*param_1 != param_4);
        (*API_GDI32_DLL_CreateRectRgn)(iVar1,param_3 - local_18,local_1c,(param_2 - local_18) + -1);
        local_10 = FUN__text__0056ce80();
        (*API_GDI32_DLL_CombineRgn)(local_c,local_c,local_10,2);
        FUN__text__0056ce80();
        (*API_GDI32_DLL_DeleteObject)(local_10);
        FUN__text__0056ce80();
      }
      param_1 = param_1 + 1;
    }
    local_18 = local_18 + 1;
  } while( true );
}

