
void text_render_B(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 auStack_c0 [16];
  int iStack_80;
  int iStack_7c;
  int iStack_78;
  int iStack_74;
  undefined4 uStack_70;
  int iStack_6c;
  int iStack_68;
  int iStack_64;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  uint uStack_58;
  int iStack_54;
  int iStack_50;
  uint uStack_4c;
  int iStack_48;
  uint uStack_44;
  undefined1 auStack_40 [4];
  undefined4 uStack_3c;
  undefined *puStack_38;
  int iStack_34;
  undefined2 uStack_30;
  undefined2 uStack_2e;
  undefined4 uStack_2c;
  int iStack_10;
  int iStack_c;
  int iStack_8;
  
  puVar5 = auStack_c0;
  for (iVar4 = 0x2f; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  iStack_c = 0;
  iStack_10 = 0;
  uStack_5c = 0;
  uStack_60 = 0;
  uStack_70 = 1;
  FUN_00403730();
  iStack_c = func_0x00414440();
  (*API_GDI32_DLL_SelectObject)(iStack_c,param_2);
  iStack_74 = __chkesp();
  if ((iStack_74 == 0) &&
     (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                           DAT_005ff0ac + 0x2c,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  (*API_KERNEL32_DLL_lstrlenA)(param_3,&uStack_58);
  uVar3 = __chkesp();
  (*API_GDI32_DLL_GetTextExtentPoint32A)(iStack_c,param_3,uVar3);
  iStack_7c = __chkesp();
  if ((iStack_7c == 0) &&
     (iVar4 = FUN_00424f80("tret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                           DAT_005ff0ac + 0x2f,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  (*API_GDI32_DLL_SelectObject)(iStack_c,iStack_74);
  iStack_74 = __chkesp();
  if ((iStack_74 == 0) &&
     (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                           DAT_005ff0ac + 0x32,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  iStack_6c = iStack_54 / 10;
  if (iStack_6c == 0) {
    iStack_6c = 1;
  }
  if (3 < iStack_6c) {
    iStack_6c = 3;
  }
  uStack_58 = uStack_58 + iStack_6c * 2;
  iStack_54 = iStack_54 + iStack_6c * 2;
  if (((int)(0x100 / (longlong)iStack_54) + 1) * 0x100 < (int)uStack_58) {
    uStack_58 = ((int)(0x100 / (longlong)iStack_54) + 1) * 0x100;
  }
  uStack_4c = uStack_58;
  iStack_50 = iStack_54;
  _memset(&uStack_3c,0,0x28);
  uStack_3c = 0x28;
  puStack_38 = (undefined *)uStack_4c;
  iStack_34 = -iStack_50;
  uStack_30 = 1;
  uStack_2c = 0;
  uStack_2e = 0x20;
  (*API_GDI32_DLL_CreateCompatibleDC)(0);
  iStack_c = __chkesp();
  if ((iStack_c == 0) &&
     (iVar4 = FUN_00424f80("hDC!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                           DAT_005ff0ac + 0x4b,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (iStack_c != 0) {
    (*API_GDI32_DLL_CreateDIBSection)(iStack_c,&uStack_3c,0,auStack_40,0,0);
    iStack_10 = __chkesp();
    if ((iStack_10 == 0) &&
       (iVar4 = FUN_00424f80("hbmBitmap!=0",
                             "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                             DAT_005ff0ac + 0x4e,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (iStack_10 != 0) {
      (*API_GDI32_DLL_SelectObject)(iStack_c,iStack_10);
      iStack_74 = __chkesp();
      if ((iStack_74 == 0) &&
         (iVar4 = FUN_00424f80("bhGdiObj!=0",
                               "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0ac + 0x52,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_GDI32_DLL_SetMapMode)(iStack_c,1);
      iStack_68 = __chkesp();
      if ((iStack_68 == 0) &&
         (iVar4 = FUN_00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0ac + 0x55,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_GDI32_DLL_GetStockObject)(4);
      uVar3 = __chkesp();
      (*API_GDI32_DLL_SelectObject)(iStack_c,uVar3);
      iStack_78 = __chkesp();
      if ((iStack_78 == 0) &&
         (iVar4 = FUN_00424f80("hGdiRet!=0",
                               "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0ac + 0x58,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_GDI32_DLL_PatBlt)(iStack_c,0,0,uStack_4c,iStack_50,0xf00021);
      iStack_7c = __chkesp();
      if ((iStack_7c == 0) &&
         (iVar4 = FUN_00424f80("tret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0ac + 0x5a,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_GDI32_DLL_SelectObject)(iStack_c,param_2);
      iStack_78 = __chkesp();
      if ((iStack_78 == 0) &&
         (iVar4 = FUN_00424f80("hGdiRet!=0",
                               "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0ac + 0x5d,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_GDI32_DLL_SetBkMode)(iStack_c,1);
      iStack_68 = __chkesp();
      if ((iStack_68 == 0) &&
         (iVar4 = FUN_00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0ac + 0x60,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_GDI32_DLL_SetBkColor)(iStack_c,0);
      __chkesp();
      (*API_GDI32_DLL_SetTextAlign)(iStack_c,0);
      __chkesp();
      iStack_80 = param_4;
      if (param_4 == 1) {
        (*API_GDI32_DLL_SetTextColor)(iStack_c,0x80808);
        __chkesp();
        (*API_KERNEL32_DLL_lstrlenA)(param_3);
        uVar3 = __chkesp();
        (*API_GDI32_DLL_TextOutA)(iStack_c,0,iStack_6c,param_3,uVar3);
        __chkesp();
        (*API_KERNEL32_DLL_lstrlenA)(param_3);
        uVar3 = __chkesp();
        (*API_GDI32_DLL_TextOutA)(iStack_c,iStack_6c * 2,iStack_6c,param_3,uVar3);
        __chkesp();
        (*API_KERNEL32_DLL_lstrlenA)(param_3);
        uVar3 = __chkesp();
        (*API_GDI32_DLL_TextOutA)(iStack_c,iStack_6c,0,param_3,uVar3);
        __chkesp();
        (*API_KERNEL32_DLL_lstrlenA)(param_3);
        uVar3 = __chkesp();
        (*API_GDI32_DLL_TextOutA)(iStack_c,iStack_6c,iStack_6c * 2,param_3,uVar3);
        __chkesp();
      }
      else if (param_4 == 2) {
        (*API_GDI32_DLL_SetTextColor)(iStack_c,0x80808);
        __chkesp();
        (*API_KERNEL32_DLL_lstrlenA)(param_3);
        uVar3 = __chkesp();
        (*API_GDI32_DLL_TextOutA)(iStack_c,iStack_6c * 2,iStack_6c * 2,param_3,uVar3);
        __chkesp();
      }
      (*API_GDI32_DLL_SetTextColor)(iStack_c,0xffffff);
      __chkesp();
      (*API_KERNEL32_DLL_lstrlenA)(param_3);
      uVar3 = __chkesp();
      (*API_GDI32_DLL_TextOutA)(iStack_c,iStack_6c,iStack_6c,param_3,uVar3);
      __chkesp();
      uStack_44 = uStack_58;
      uVar2 = uStack_44;
      iStack_48 = iStack_54;
      iVar4 = iStack_48;
      uStack_44._0_2_ = (undefined2)uStack_58;
      *(undefined2 *)(iStack_8 + 0x40) = (undefined2)uStack_44;
      iStack_48._0_2_ = (short)iStack_54;
      *(short *)(iStack_8 + 0x42) = (short)iStack_48;
      iStack_64 = (uStack_58 >> 8) + 1;
      if (uStack_58 < 0x100) {
        *(undefined2 *)(iStack_8 + 0x38) = (undefined2)uStack_44;
      }
      else {
        *(undefined2 *)(iStack_8 + 0x38) = 0x100;
      }
      *(short *)(iStack_8 + 0x3a) = (short)iStack_64 * (short)iStack_48;
      if (0xff < *(short *)(iStack_8 + 0x3a)) {
        *(undefined2 *)(iStack_8 + 0x3a) = 0x100;
      }
      *(undefined4 *)(iStack_8 + 0x34) = 0x19;
      iStack_48 = iVar4;
      uStack_44 = uVar2;
      iStack_68 = func_0x00403bd0(param_1,0);
      if (iStack_68 == 0) {
        *(ushort *)(iStack_8 + 0x44) = *(ushort *)(iStack_8 + 0x44) | 4;
        uStack_70 = 0;
      }
    }
  }
  if ((iStack_74 == 0) &&
     (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                           DAT_005ff0ac + 0xc5,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  (*API_GDI32_DLL_SelectObject)(iStack_c,iStack_74);
  iStack_74 = __chkesp();
  if ((iStack_74 == 0) &&
     (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                           DAT_005ff0ac + 199,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (iStack_10 != 0) {
    (*API_GDI32_DLL_DeleteObject)(iStack_10);
    iStack_68 = __chkesp();
    if ((iStack_68 == 0) &&
       (iVar4 = FUN_00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                             DAT_005ff0ac + 0xcb,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (iStack_c != 0) {
    (*API_GDI32_DLL_DeleteDC)(iStack_c);
    iStack_68 = __chkesp();
    if ((iStack_68 == 0) &&
       (iVar4 = FUN_00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                             DAT_005ff0ac + 0xcf,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  puStack_38 = &UNK_004075d8;
  __chkesp();
  return;
}

