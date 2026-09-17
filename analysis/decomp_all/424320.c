
void FUN__text__00424320(int *param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_9c [16];
  int local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined2 local_4c;
  undefined2 local_4a;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  int local_30;
  undefined4 local_2c;
  undefined4 local_28;
  int local_24;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_8;
  
  puVar2 = local_9c;
  for (iVar1 = 0x26; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_24 = 0;
  local_28 = 0;
  local_2c = 0;
  if (param_1[3] != 0) {
    local_1c = *(undefined4 *)(*param_1 + 4);
    local_18 = *(undefined4 *)(*param_1 + 8);
    local_30 = 0;
    local_5c = 1;
    (*API_GDI32_DLL_CreateCompatibleDC)(0);
    local_30 = FUN__text__0056ce80();
    if (local_30 != 0) {
      local_58 = 0x28;
      local_54 = local_1c;
      local_50 = local_18;
      local_4c = 1;
      local_4a = 0x20;
      local_48 = 0;
      local_44 = 0;
      local_40 = 0;
      local_3c = 0;
      local_38 = 0;
      local_34 = 0;
      (*API_GDI32_DLL_CreateDIBSection)(local_30,&local_58,0,&local_28,0,0);
      local_24 = FUN__text__0056ce80();
      if (local_24 != 0) {
        (*API_GDI32_DLL_SelectObject)(local_30,local_24);
        FUN__text__0056ce80();
        (*API_GDI32_DLL_BitBlt)(local_30,0,0,local_1c,local_18,param_1[2],0,0,0xcc0020);
        local_5c = FUN__text__0056ce80();
      }
    }
    if (local_30 != 0) {
      (*API_GDI32_DLL_DeleteDC)(local_30);
      FUN__text__0056ce80();
    }
    if (local_5c == 0) {
      (*API_GDI32_DLL_DeleteObject)(local_24);
      FUN__text__0056ce80();
      local_24 = 0;
      local_28 = 0;
    }
    if (local_24 != 0) {
      local_2c = FUN__text__00424510(local_28,local_1c,local_18,param_2);
      (*API_GDI32_DLL_DeleteObject)(local_24);
      FUN__text__0056ce80();
    }
  }
  local_8 = 0x424500;
  FUN__text__0056ce80();
  return;
}

