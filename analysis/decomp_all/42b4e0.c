
void __thiscall FUN__text__0042b4e0(int *param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int *local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    (*API_USER32_DLL_GetWindowLongA)(param_2,0xfffffffa);
    local_14 = FUN__text__0056ce80();
    (*API_USER32_DLL_LoadMenuA)(PTR_IMAGE_DOS_HEADER_007a2728,local_8[0x18]);
    local_c = FUN__text__0056ce80();
    (*API_USER32_DLL_GetSubMenu)(local_c,0);
    local_10 = FUN__text__0056ce80();
    (*API_USER32_DLL_GetPhysicalCursorPos)(&local_1c);
    FUN__text__0056ce80();
    (*API_USER32_DLL_SetForegroundWindow)(param_2);
    FUN__text__0056ce80();
    (*API_USER32_DLL_TrackPopupMenu)(local_10,0x20,local_1c,local_18,0,param_2,0);
    FUN__text__0056ce80();
    (*API_USER32_DLL_DestroyMenu)(local_c);
    FUN__text__0056ce80();
  }
  local_8 = (int *)0x42b5cd;
  FUN__text__0056ce80();
  return;
}

