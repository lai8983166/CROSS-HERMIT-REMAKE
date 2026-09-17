
void FUN__text__004232f0(uint *param_1,int param_2,int param_3,uint param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  uint local_18;
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_18 = (param_4 & 0xff) << 0x10 | ((int)(param_4 & 0xffff) >> 8) << 8 | param_4 >> 0x10 & 0xff
  ;
  if (local_18 == 0xffffffff) {
    local_18 = *param_1;
  }
  (*API_GDI32_DLL_CreateRectRgn)(0,0,0,0);
  local_c = FUN__text__0056ce80();
  local_1c = 0;
  do {
    if (param_3 <= local_1c) {
      local_18 = 0x423470;
      FUN__text__0056ce80();
      return;
    }
    for (local_20 = 0; iVar1 = local_20, local_20 < param_2; local_20 = local_20 + 1) {
      if (*param_1 != local_18) {
        local_14 = local_20;
        do {
          local_20 = local_20 + 1;
          if (param_2 <= local_20) break;
          param_1 = param_1 + 1;
        } while (*param_1 != local_18);
        (*API_GDI32_DLL_CreateRectRgn)(iVar1,param_3 - local_1c,local_20,(param_2 - local_1c) + -1);
        local_10 = FUN__text__0056ce80();
        (*API_GDI32_DLL_CombineRgn)(local_c,local_c,local_10,2);
        FUN__text__0056ce80();
        (*API_GDI32_DLL_DeleteObject)(local_10);
        FUN__text__0056ce80();
      }
      param_1 = param_1 + 1;
    }
    local_1c = local_1c + 1;
  } while( true );
}

