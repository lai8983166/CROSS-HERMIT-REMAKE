
void blit_0x422cd0(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 auStack_a0 [16];
  int iStack_60;
  undefined4 uStack_5c;
  undefined4 uStack_58;
  undefined4 uStack_54;
  undefined2 uStack_50;
  undefined2 uStack_4e;
  undefined4 uStack_4c;
  undefined4 uStack_48;
  undefined4 uStack_44;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  int iStack_34;
  int iStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  int iStack_24;
  undefined1 auStack_20 [4];
  undefined4 uStack_1c;
  undefined4 uStack_18;
  undefined *puStack_8;
  
  puVar2 = auStack_a0;
  for (iVar1 = 0x27; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iStack_24 = 0;
  uStack_28 = 0;
  uStack_2c = 0;
  if (param_1 != 0) {
    (*API_GDI32_DLL_GetObjectA)(param_1,0x18,auStack_20);
    iVar1 = __chkesp();
    if (iVar1 != 0) {
      iStack_30 = 0;
      iStack_34 = 0;
      iStack_60 = 1;
      (*API_GDI32_DLL_CreateCompatibleDC)(0);
      iStack_30 = __chkesp();
      if (iStack_30 != 0) {
        uStack_5c = 0x28;
        uStack_58 = uStack_1c;
        uStack_54 = uStack_18;
        uStack_50 = 1;
        uStack_4e = 0x20;
        uStack_4c = 0;
        uStack_48 = 0;
        uStack_44 = 0;
        uStack_40 = 0;
        uStack_3c = 0;
        uStack_38 = 0;
        (*API_GDI32_DLL_CreateDIBSection)(iStack_30,&uStack_5c,0,&uStack_28,0,0);
        iStack_24 = __chkesp();
        if (iStack_24 != 0) {
          (*API_GDI32_DLL_SelectObject)(iStack_30,iStack_24);
          __chkesp();
          (*API_GDI32_DLL_CreateCompatibleDC)(iStack_30);
          iStack_34 = __chkesp();
          if (iStack_34 != 0) {
            (*API_GDI32_DLL_SelectObject)(iStack_34,param_1);
            __chkesp();
            (*API_GDI32_DLL_BitBlt)(iStack_30,0,0,uStack_1c,uStack_18,iStack_34,0,0,0xcc0020);
            iStack_60 = __chkesp();
          }
        }
      }
      if (iStack_34 != 0) {
        (*API_GDI32_DLL_DeleteDC)(iStack_34);
        __chkesp();
      }
      if (iStack_30 != 0) {
        (*API_GDI32_DLL_DeleteDC)(iStack_30);
        __chkesp();
      }
      if (iStack_60 == 0) {
        (*API_GDI32_DLL_DeleteObject)(iStack_24);
        __chkesp();
        iStack_24 = 0;
        uStack_28 = 0;
      }
      if (iStack_24 != 0) {
        uStack_2c = func_0x004232f0(uStack_28,uStack_1c,uStack_18,param_2);
        (*API_GDI32_DLL_DeleteObject)(iStack_24);
        __chkesp();
      }
    }
  }
  puStack_8 = &UNK_00422f18;
  __chkesp();
  return;
}

