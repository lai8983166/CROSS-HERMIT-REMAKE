
void __thiscall text_render_font(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 auStack_1e8 [16];
  int iStack_1a8;
  undefined4 uStack_1a4;
  uint uStack_1a0;
  undefined4 uStack_19c;
  int iStack_198;
  undefined4 uStack_194;
  uint uStack_190;
  undefined4 uStack_18c;
  int iStack_188;
  undefined4 uStack_184;
  uint uStack_180;
  undefined4 uStack_17c;
  int iStack_178;
  undefined4 uStack_174;
  uint uStack_170;
  undefined4 uStack_16c;
  int iStack_168;
  undefined4 uStack_164;
  uint uStack_160;
  undefined4 uStack_15c;
  undefined1 uStack_158;
  undefined3 uStack_157;
  ushort *puStack_154;
  ushort *puStack_150;
  int iStack_14c;
  ushort *puStack_148;
  char cStack_144;
  int iStack_140;
  int iStack_13c;
  undefined2 auStack_138 [2];
  uint uStack_134;
  uint uStack_130;
  int iStack_12c;
  uint uStack_128;
  int iStack_124;
  int iStack_120;
  undefined4 uStack_11c;
  undefined4 uStack_118;
  undefined4 uStack_114;
  undefined4 uStack_110;
  undefined4 uStack_10c;
  int iStack_108;
  undefined2 uStack_104;
  undefined2 uStack_102;
  undefined4 uStack_100;
  int iStack_e4;
  undefined1 auStack_e0 [88];
  uint uStack_88;
  undefined *puStack_30;
  int iStack_c;
  int iStack_8;
  
  puVar4 = auStack_1e8;
  for (iVar2 = 0x79; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  *(undefined4 *)(param_1 + 0x58) = param_2;
  *(undefined4 *)(param_1 + 0x6c) = 0x3f800000;
  if (*(uint *)(param_1 + 0x50) < 0x29) {
    if (*(uint *)(param_1 + 0x50) < 0x15) {
      *(undefined4 *)(param_1 + 0x68) = 0x100;
      *(undefined4 *)(param_1 + 100) = 0x100;
    }
    else {
      *(undefined4 *)(param_1 + 0x68) = 0x200;
      *(undefined4 *)(param_1 + 100) = 0x200;
    }
  }
  else {
    *(undefined4 *)(param_1 + 0x68) = 0x400;
    *(undefined4 *)(param_1 + 100) = 0x400;
  }
  iStack_8 = param_1;
  (**(code **)(**(int **)(param_1 + 0x58) + 0x1c))(*(undefined4 *)(param_1 + 0x58),auStack_e0);
  __chkesp();
  if (uStack_88 < *(uint *)(iStack_8 + 100)) {
    uStack_160 = uStack_88;
    uStack_15c = 0;
    iStack_168 = *(int *)(iStack_8 + 100);
    uStack_164 = 0;
    *(float *)(iStack_8 + 0x6c) = (float)uStack_88 / (float)iStack_168;
    *(uint *)(iStack_8 + 0x68) = uStack_88;
    *(uint *)(iStack_8 + 100) = uStack_88;
  }
  (**(code **)(**(int **)(iStack_8 + 0x58) + 0x50))
            (*(undefined4 *)(iStack_8 + 0x58),*(undefined4 *)(iStack_8 + 100),
             *(undefined4 *)(iStack_8 + 0x68),1,0,0x1a,1,iStack_8 + 0x5c);
  iStack_c = __chkesp();
  if (-1 < iStack_c) {
    _memset(&uStack_110,0,0x28);
    uStack_110 = 0x28;
    uStack_10c = *(undefined4 *)(iStack_8 + 100);
    iStack_108 = -*(int *)(iStack_8 + 0x68);
    uStack_104 = 1;
    uStack_100 = 0;
    uStack_102 = 0x20;
    (*API_GDI32_DLL_CreateCompatibleDC)(0);
    uStack_114 = __chkesp();
    (*API_GDI32_DLL_CreateDIBSection)(uStack_114,&uStack_110,0,&iStack_e4,0,0);
    uStack_118 = __chkesp();
    (*API_GDI32_DLL_SetMapMode)(uStack_114,1);
    __chkesp();
    uStack_11c = 0x60;
    uVar1 = func_0x0056cfcc(0x48);
    (*API_KERNEL32_DLL_MulDiv)(*(undefined4 *)(iStack_8 + 0x50),uVar1);
    iStack_120 = __chkesp();
    iStack_120 = -iStack_120;
    iStack_124 = (-(uint)((*(uint *)(iStack_8 + 0x54) & 1) != 0) & 300) + 400;
    uStack_128 = (uint)((*(uint *)(iStack_8 + 0x54) & 2) != 0);
    (*API_GDI32_DLL_CreateFontA)(iStack_120,0,0,0,iStack_124,uStack_128,0,0,1,0,0,4,2,iStack_8);
    iStack_12c = __chkesp();
    if (iStack_12c != 0) {
      (*API_GDI32_DLL_SelectObject)(uStack_114,uStack_118);
      __chkesp();
      (*API_GDI32_DLL_SelectObject)(uStack_114,iStack_12c);
      __chkesp();
      (*API_GDI32_DLL_SetTextColor)(uStack_114,0xffffff);
      __chkesp();
      (*API_GDI32_DLL_SetBkColor)(uStack_114,0);
      __chkesp();
      (*API_GDI32_DLL_SetTextAlign)(uStack_114,0);
      __chkesp();
      uStack_130 = 0;
      uStack_134 = 0;
      auStack_138[0] = DAT_005924bc;
      for (cStack_144 = ' '; cStack_144 < '\x7f'; cStack_144 = cStack_144 + '\x01') {
        auStack_138[0] = CONCAT11(auStack_138[0]._1_1_,cStack_144);
        (*API_GDI32_DLL_GetTextExtentPoint32A)(uStack_114,auStack_138,1,&iStack_140);
        __chkesp();
        if (*(uint *)(iStack_8 + 100) < uStack_130 + 1 + iStack_140) {
          uStack_130 = 0;
          uStack_134 = uStack_134 + 1 + iStack_13c;
        }
        (*API_GDI32_DLL_ExtTextOutA)(uStack_114,uStack_130,uStack_134,2,0,auStack_138,1,0);
        __chkesp();
        uStack_170 = uStack_130;
        uStack_16c = 0;
        iStack_178 = *(int *)(iStack_8 + 100);
        uStack_174 = 0;
        *(float *)(iStack_8 + 0x70 + (cStack_144 + -0x20) * 0x10) =
             (float)uStack_130 / (float)iStack_178;
        uStack_180 = uStack_134;
        uStack_17c = 0;
        iStack_188 = *(int *)(iStack_8 + 0x68);
        uStack_184 = 0;
        *(float *)(iStack_8 + 0x74 + (cStack_144 + -0x20) * 0x10) =
             (float)uStack_134 / (float)iStack_188;
        uStack_190 = uStack_130 + iStack_140;
        uStack_18c = 0;
        iStack_198 = *(int *)(iStack_8 + 100);
        uStack_194 = 0;
        *(float *)(iStack_8 + 0x78 + (cStack_144 + -0x20) * 0x10) =
             (float)uStack_190 / (float)iStack_198;
        uStack_1a0 = uStack_134 + iStack_13c;
        uStack_19c = 0;
        iStack_1a8 = *(int *)(iStack_8 + 0x68);
        uStack_1a4 = 0;
        *(float *)(iStack_8 + 0x7c + (cStack_144 + -0x20) * 0x10) =
             (float)uStack_1a0 / (float)iStack_1a8;
        uStack_130 = uStack_130 + 1 + iStack_140;
      }
      (**(code **)(**(int **)(iStack_8 + 0x5c) + 0x40))
                (*(undefined4 *)(iStack_8 + 0x5c),0,&iStack_14c,0,0);
      __chkesp();
      puStack_150 = puStack_148;
      for (uStack_134 = 0; uStack_134 < *(uint *)(iStack_8 + 0x68); uStack_134 = uStack_134 + 1) {
        puStack_154 = puStack_150;
        for (uStack_130 = 0; uStack_130 < *(uint *)(iStack_8 + 100); uStack_130 = uStack_130 + 1) {
          uVar3 = (*(uint *)(iStack_e4 + (*(int *)(iStack_8 + 100) * uStack_134 + uStack_130) * 4) &
                  0xff) >> 4;
          _uStack_158 = CONCAT31(uStack_157,(char)uVar3);
          if (uVar3 == 0) {
            *puStack_154 = 0;
          }
          else {
            *puStack_154 = (ushort)(uVar3 << 0xc) | 0xfff;
          }
          puStack_154 = puStack_154 + 1;
        }
        puStack_150 = (ushort *)((int)puStack_150 + iStack_14c);
      }
      (**(code **)(**(int **)(iStack_8 + 0x5c) + 0x44))(*(undefined4 *)(iStack_8 + 0x5c),0);
      __chkesp();
      (*API_GDI32_DLL_DeleteObject)(uStack_118);
      __chkesp();
      (*API_GDI32_DLL_DeleteDC)(uStack_114);
      __chkesp();
      (*API_GDI32_DLL_DeleteObject)(iStack_12c);
      __chkesp();
    }
  }
  puStack_30 = &UNK_0040180a;
  __chkesp();
  return;
}

