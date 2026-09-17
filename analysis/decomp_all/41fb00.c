
void FUN__text__0041fb00(undefined4 param_1,undefined4 param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  int *local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__00428a40(0x428);
  *local_8 = local_10;
  if (*local_8 != 0) {
    *(undefined4 *)*local_8 = 0x28;
    *(undefined4 *)(*local_8 + 4) = param_1;
    *(undefined4 *)(*local_8 + 8) = param_2;
    *(undefined2 *)(*local_8 + 0xc) = 1;
    *(undefined2 *)(*local_8 + 0xe) = param_3;
    *(undefined4 *)(*local_8 + 0x10) = 0;
    *(undefined4 *)(*local_8 + 0x14) = 0;
    *(undefined4 *)(*local_8 + 0x18) = 0;
    *(undefined4 *)(*local_8 + 0x1c) = 0;
    *(undefined4 *)(*local_8 + 0x20) = 0;
    *(undefined4 *)(*local_8 + 0x24) = 0;
    (*API_USER32_DLL_GetDC)(0);
    local_c = FUN__text__0056ce80();
    (*API_GDI32_DLL_CreateDIBSection)(local_c,*local_8,0,local_8 + 1,0,0);
    iVar1 = FUN__text__0056ce80();
    local_8[3] = iVar1;
    (*API_GDI32_DLL_CreateCompatibleDC)(local_c);
    iVar1 = FUN__text__0056ce80();
    local_8[2] = iVar1;
    (*API_USER32_DLL_ReleaseDC)(0,local_c);
    FUN__text__0056ce80();
  }
  local_8 = (int *)0x41fc45;
  FUN__text__0056ce80();
  return;
}

