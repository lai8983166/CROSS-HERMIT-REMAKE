
void blit_0x423100(int *param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 auStack_9c [16];
  int iStack_5c;
  undefined4 uStack_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined2 uStack_4c;
  undefined2 uStack_4a;
  undefined4 uStack_48;
  undefined4 uStack_44;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  undefined4 uStack_34;
  int iStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  int iStack_24;
  undefined4 uStack_1c;
  undefined4 uStack_18;
  undefined *puStack_8;
  
  puVar2 = auStack_9c;
  for (iVar1 = 0x26; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iStack_24 = 0;
  uStack_28 = 0;
  uStack_2c = 0;
  if (param_1[3] != 0) {
    uStack_1c = *(undefined4 *)(*param_1 + 4);
    uStack_18 = *(undefined4 *)(*param_1 + 8);
    iStack_30 = 0;
    iStack_5c = 1;
    (*API_GDI32_DLL_CreateCompatibleDC)(0);
    iStack_30 = __chkesp();
    if (iStack_30 != 0) {
      uStack_58 = 0x28;
      uStack_54 = uStack_1c;
      uStack_50 = uStack_18;
      uStack_4c = 1;
      uStack_4a = 0x20;
      uStack_48 = 0;
      uStack_44 = 0;
      uStack_40 = 0;
      uStack_3c = 0;
      uStack_38 = 0;
      uStack_34 = 0;
      (*API_GDI32_DLL_CreateDIBSection)(iStack_30,&uStack_58,0,&uStack_28,0,0);
      iStack_24 = __chkesp();
      if (iStack_24 != 0) {
        (*API_GDI32_DLL_SelectObject)(iStack_30,iStack_24);
        __chkesp();
        (*API_GDI32_DLL_BitBlt)(iStack_30,0,0,uStack_1c,uStack_18,param_1[2],0,0,0xcc0020);
        iStack_5c = __chkesp();
      }
    }
    if (iStack_30 != 0) {
      (*API_GDI32_DLL_DeleteDC)(iStack_30);
      __chkesp();
    }
    if (iStack_5c == 0) {
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
  puStack_8 = &UNK_004232e0;
  __chkesp();
  return;
}

