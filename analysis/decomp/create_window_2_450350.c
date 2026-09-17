
void __thiscall
create_window_2(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 auStack_88 [16];
  undefined *puStack_48;
  undefined4 uStack_44;
  code *pcStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  undefined *puStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  undefined4 uStack_24;
  char *pcStack_20;
  undefined4 uStack_1c;
  int iStack_18;
  int iStack_14;
  int iStack_10;
  int iStack_c;
  int iStack_8;
  
  puVar3 = auStack_88;
  for (iVar2 = 0x21; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iStack_8 = param_1;
  (*API_USER32_DLL_SetRect)(param_1 + 0x8bc,param_2,param_3,param_4,param_5);
  __chkesp();
  iStack_18 = *(int *)(iStack_8 + 0x8bc);
  iStack_14 = *(int *)(iStack_8 + 0x8c0);
  iStack_10 = *(int *)(iStack_8 + 0x8c4);
  iStack_c = *(int *)(iStack_8 + 0x8c8);
  (*API_USER32_DLL_AdjustWindowRect)(&iStack_18,param_6,0);
  __chkesp();
  puStack_48 = (undefined *)0x30;
  uStack_44 = 0;
  pcStack_20 = "Cross Hermit";
  pcStack_40 = wndproc_2;
  puStack_34 = PTR_IMAGE_DOS_HEADER_007a2728;
  uStack_3c = 0;
  uStack_38 = 0;
  (*API_USER32_DLL_LoadIconA)(PTR_IMAGE_DOS_HEADER_007a2728,0x9d);
  uStack_30 = __chkesp();
  (*API_USER32_DLL_LoadIconA)(PTR_IMAGE_DOS_HEADER_007a2728,0x9d);
  uStack_1c = __chkesp();
  (*API_USER32_DLL_LoadCursorA)(0,0x7f00);
  uStack_2c = __chkesp();
  (*API_GDI32_DLL_GetStockObject)(4);
  uStack_28 = __chkesp();
  uStack_24 = 0;
  (*API_USER32_DLL_RegisterClassExA)(&puStack_48);
  sVar1 = __chkesp();
  if (sVar1 != 0) {
    (*API_USER32_DLL_CreateWindowExA)
              (0,"Cross Hermit","Cross Hermit",param_6,0x10,0x10,iStack_10 - iStack_18,
               iStack_c - iStack_14,0,0,PTR_IMAGE_DOS_HEADER_007a2728,iStack_8);
    PTR_DAT_007a0bb4 = (undefined *)__chkesp();
    if (PTR_DAT_007a0bb4 != (undefined *)0x0) {
      (*API_USER32_DLL_ShowWindow)(PTR_DAT_007a0bb4,param_7);
      __chkesp();
      (*API_USER32_DLL_UpdateWindow)(PTR_DAT_007a0bb4);
      __chkesp();
      (*API_USER32_DLL_GetClientRect)(PTR_DAT_007a0bb4,&iStack_18);
      __chkesp();
      (*API_USER32_DLL_GetWindowRect)(PTR_DAT_007a0bb4,&iStack_18);
      __chkesp();
    }
  }
  puStack_48 = &UNK_00450566;
  __chkesp();
  return;
}

