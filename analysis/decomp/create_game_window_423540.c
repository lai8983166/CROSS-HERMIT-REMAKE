
void __fastcall create_game_window(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (param_1[2] != 0) {
    (*API_GDI32_DLL_DeleteDC)(param_1[2]);
    __chkesp();
  }
  if (*local_8 != 0) {
    (*API_USER32_DLL_UnregisterClassA)("Cross Hermit",PTR_IMAGE_DOS_HEADER_007a2728);
    __chkesp();
  }
  if (local_8[5] != 0) {
    (*API_GDI32_DLL_DeleteObject)(local_8[5]);
    __chkesp();
  }
  local_8[2] = 0;
  *local_8 = 0;
  local_8[5] = 0;
  local_8 = (int *)0x4235ea;
  __chkesp();
  return;
}

