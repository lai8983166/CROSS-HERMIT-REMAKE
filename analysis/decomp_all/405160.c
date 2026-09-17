
void text_render_A(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 auStack_f0 [16];
  int iStack_b0;
  undefined4 uStack_ac;
  int iStack_a8;
  int aiStack_9c [3];
  int iStack_90;
  int iStack_8c;
  undefined1 auStack_88 [8];
  int iStack_80;
  int iStack_7c;
  int iStack_78;
  undefined4 uStack_74;
  int iStack_70;
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
  undefined4 uStack_40;
  undefined4 uStack_3c;
  uint uStack_38;
  int iStack_34;
  undefined2 uStack_30;
  undefined2 uStack_2e;
  undefined4 uStack_2c;
  int iStack_10;
  undefined *puStack_c;
  int iStack_8;
  
  puVar5 = auStack_f0;
  for (iVar4 = 0x3b; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  puStack_c = (undefined *)0x0;
  iStack_10 = 0;
  uStack_5c = 0;
  uStack_60 = 0;
  uStack_74 = 1;
  FUN_00403730();
  (*API_KERNEL32_DLL_lstrlenA)(param_3);
  iVar4 = __chkesp();
  if (iVar4 != 0) {
    puStack_c = (undefined *)func_0x00414440();
    (*API_GDI32_DLL_SelectObject)(puStack_c,param_2);
    iStack_78 = __chkesp();
    if ((iStack_78 == 0) &&
       (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp"
                             ,DAT_005ff0a8 + 0x2e,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (*API_KERNEL32_DLL_lstrlenA)(param_3,&uStack_58);
    uVar3 = __chkesp();
    (*API_GDI32_DLL_GetTextExtentPoint32A)(puStack_c,param_3,uVar3);
    iStack_80 = __chkesp();
    if ((iStack_80 == 0) &&
       (iVar4 = FUN_00424f80("tret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                             DAT_005ff0a8 + 0x31,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (*API_GDI32_DLL_SelectObject)(puStack_c,iStack_78);
    iStack_78 = __chkesp();
    if ((iStack_78 == 0) &&
       (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp"
                             ,DAT_005ff0a8 + 0x34,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    iStack_70 = iStack_54 / 10;
    if (iStack_70 == 0) {
      iStack_70 = 1;
    }
    if (3 < iStack_70) {
      iStack_70 = 3;
    }
    uStack_58 = uStack_58 + iStack_70 * 2;
    iStack_54 = iStack_54 + iStack_70 * 2;
    if (((int)(0x100 / (longlong)iStack_54) + 1) * 0x100 < (int)uStack_58) {
      uStack_58 = ((int)(0x100 / (longlong)iStack_54) + 1) * 0x100;
    }
    uStack_4c = uStack_58;
    iStack_50 = iStack_54;
    _memset(&uStack_3c,0,0x28);
    uStack_3c = 0x28;
    uStack_38 = uStack_4c;
    iStack_34 = -iStack_50;
    uStack_30 = 1;
    uStack_2c = 0;
    uStack_2e = 0x20;
    (*API_GDI32_DLL_CreateCompatibleDC)(0);
    puStack_c = (undefined *)__chkesp();
    if ((puStack_c == (undefined *)0x0) &&
       (iVar4 = FUN_00424f80("hDC!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                             DAT_005ff0a8 + 0x4d,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (puStack_c != (undefined *)0x0) {
      (*API_GDI32_DLL_CreateDIBSection)(puStack_c,&uStack_3c,0,&uStack_40,0,0);
      iStack_10 = __chkesp();
      if ((iStack_10 == 0) &&
         (iVar4 = FUN_00424f80("hbmBitmap!=0",
                               "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0a8 + 0x50,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if (iStack_10 != 0) {
        (*API_GDI32_DLL_SelectObject)(puStack_c,iStack_10);
        iStack_78 = __chkesp();
        if ((iStack_78 == 0) &&
           (iVar4 = FUN_00424f80("bhGdiObj!=0",
                                 "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                 DAT_005ff0a8 + 0x54,0), iVar4 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        (*API_GDI32_DLL_SetMapMode)(puStack_c,1);
        iStack_6c = __chkesp();
        (*API_GDI32_DLL_GetStockObject)(4);
        uVar3 = __chkesp();
        (*API_GDI32_DLL_SelectObject)(puStack_c,uVar3);
        iStack_7c = __chkesp();
        (*API_GDI32_DLL_PatBlt)(puStack_c,0,0,uStack_4c,iStack_50,0xf00021);
        iStack_80 = __chkesp();
        (*API_GDI32_DLL_SelectObject)(puStack_c,param_2);
        iStack_7c = __chkesp();
        if ((iStack_7c == 0) &&
           (iVar4 = FUN_00424f80("hGdiRet!=0",
                                 "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                 DAT_005ff0a8 + 0x5f,0), iVar4 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        (*API_GDI32_DLL_SetBkMode)(puStack_c,1);
        iStack_6c = __chkesp();
        (*API_GDI32_DLL_SetBkColor)(puStack_c,0);
        __chkesp();
        (*API_GDI32_DLL_SetTextAlign)(puStack_c,0);
        __chkesp();
        iStack_b0 = param_4;
        if (param_4 == 1) {
          (*API_GDI32_DLL_SetTextColor)(puStack_c,0x80808);
          __chkesp();
          (*API_KERNEL32_DLL_lstrlenA)(param_3);
          uVar3 = __chkesp();
          (*API_GDI32_DLL_TextOutA)(puStack_c,0,iStack_70,param_3,uVar3);
          __chkesp();
          (*API_KERNEL32_DLL_lstrlenA)(param_3);
          uVar3 = __chkesp();
          (*API_GDI32_DLL_TextOutA)(puStack_c,iStack_70 * 2,iStack_70,param_3,uVar3);
          __chkesp();
          (*API_KERNEL32_DLL_lstrlenA)(param_3);
          uVar3 = __chkesp();
          (*API_GDI32_DLL_TextOutA)(puStack_c,iStack_70,0,param_3,uVar3);
          __chkesp();
          (*API_KERNEL32_DLL_lstrlenA)(param_3);
          uVar3 = __chkesp();
          (*API_GDI32_DLL_TextOutA)(puStack_c,iStack_70,iStack_70 * 2,param_3,uVar3);
          __chkesp();
        }
        else if (param_4 == 2) {
          (*API_GDI32_DLL_SetTextColor)(puStack_c,0x80808);
          __chkesp();
          (*API_KERNEL32_DLL_lstrlenA)(param_3);
          uVar3 = __chkesp();
          (*API_GDI32_DLL_TextOutA)(puStack_c,iStack_70 * 2,iStack_70 * 2,param_3,uVar3);
          __chkesp();
        }
        (*API_GDI32_DLL_SetTextColor)(puStack_c,0xffffff);
        __chkesp();
        (*API_KERNEL32_DLL_lstrlenA)(param_3);
        uVar3 = __chkesp();
        (*API_GDI32_DLL_TextOutA)(puStack_c,iStack_70,iStack_70,param_3,uVar3);
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
        iStack_6c = func_0x00403bd0(param_1,0);
        if ((iStack_6c == 0) && (iVar4 = func_0x00403910(auStack_88), iVar4 == 0)) {
          for (iStack_68 = 0; iStack_68 != iStack_64; iStack_68 = iStack_68 + 1) {
            if ((uint)(iStack_48 * iStack_68 + iStack_48) < 0x100) {
              if (uStack_44 + iStack_68 * -0x100 < 0x100) {
                iStack_8c = uStack_44 + iStack_68 * -0x100;
              }
              else {
                iStack_8c = 0x100;
              }
              aiStack_9c[0] = iStack_68 << 8;
              aiStack_9c[1] = 0;
              aiStack_9c[2] = iStack_8c;
              iStack_90 = iStack_48;
              uStack_ac = 0;
              iStack_a8 = iStack_48 * iStack_68;
              func_0x00405a80(uStack_40,auStack_88,uStack_44,iStack_48,aiStack_9c,&uStack_ac);
            }
          }
          iVar4 = func_0x00403990();
          if (iVar4 == 0) {
            *(ushort *)(iStack_8 + 0x44) = *(ushort *)(iStack_8 + 0x44) | 4;
            uStack_74 = 0;
          }
        }
      }
    }
    if ((iStack_78 == 0) &&
       (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp"
                             ,DAT_005ff0a8 + 0xc3,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (*API_GDI32_DLL_SelectObject)(puStack_c,iStack_78);
    iStack_78 = __chkesp();
    if ((iStack_78 == 0) &&
       (iVar4 = FUN_00424f80("bhGdiObj!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp"
                             ,DAT_005ff0a8 + 0xc5,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (iStack_10 != 0) {
      (*API_GDI32_DLL_DeleteObject)(iStack_10);
      iStack_6c = __chkesp();
      if ((iStack_6c == 0) &&
         (iVar4 = FUN_00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0a8 + 0xc9,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    if (puStack_c != (undefined *)0x0) {
      (*API_GDI32_DLL_DeleteDC)(puStack_c);
      iStack_6c = __chkesp();
      if ((iStack_6c == 0) &&
         (iVar4 = FUN_00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                               DAT_005ff0a8 + 0xcd,0), iVar4 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  puStack_c = &UNK_004059ce;
  __chkesp();
  return;
}

