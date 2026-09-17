
void blit_pipeline_A(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 auStack_50 [16];
  undefined4 uStack_10;
  undefined4 uStack_c;
  int iStack_8;
  
  puVar3 = auStack_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  (*API_USER32_DLL_GetSystemMetrics)(0x10);
  uVar1 = __chkesp();
  *(undefined4 *)(iStack_8 + 0xc) = uVar1;
  (*API_USER32_DLL_GetSystemMetrics)(0x11);
  uVar1 = __chkesp();
  *(undefined4 *)(iStack_8 + 0x10) = uVar1;
  (*API_USER32_DLL_GetDC)(param_1);
  uStack_c = __chkesp();
  (*API_GDI32_DLL_CreateCompatibleDC)(uStack_c);
  uVar1 = __chkesp();
  *(undefined4 *)(iStack_8 + 8) = uVar1;
  (*API_GDI32_DLL_CreateCompatibleBitmap)
            (uStack_c,*(undefined4 *)(iStack_8 + 0xc),*(undefined4 *)(iStack_8 + 0x10));
  uVar1 = __chkesp();
  *(undefined4 *)(iStack_8 + 4) = uVar1;
  (*API_GDI32_DLL_SelectObject)(*(undefined4 *)(iStack_8 + 8),*(undefined4 *)(iStack_8 + 4));
  __chkesp();
  (*API_GDI32_DLL_GetStockObject)(4);
  uStack_10 = __chkesp();
  (*API_GDI32_DLL_SelectObject)(*(undefined4 *)(iStack_8 + 8),uStack_10);
  __chkesp();
  (*API_GDI32_DLL_PatBlt)
            (*(undefined4 *)(iStack_8 + 8),0,0,*(undefined4 *)(iStack_8 + 0xc),
             *(undefined4 *)(iStack_8 + 0x10),0xf00021);
  __chkesp();
  (*API_USER32_DLL_ReleaseDC)(param_1,uStack_c);
  __chkesp();
  __chkesp();
  return;
}

