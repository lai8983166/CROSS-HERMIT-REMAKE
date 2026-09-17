
void __thiscall blit_0x420210(int param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 auStack_78 [16];
  int iStack_38;
  uint uStack_34;
  undefined4 *puStack_30;
  undefined4 *puStack_2c;
  int iStack_28;
  undefined1 *puStack_24;
  int iStack_20;
  undefined4 uStack_1c;
  undefined4 *puStack_18;
  undefined1 *puStack_14;
  int iStack_10;
  undefined4 *puStack_c;
  undefined *puStack_8;
  
  puVar4 = auStack_78;
  for (iVar2 = 0x1d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(int *)(param_1 + 0xc) != 0) {
    iStack_10 = param_2;
    puStack_8 = (undefined *)param_1;
    iVar2 = func_0x004209f0(param_2);
    if (iVar2 == 0) {
      func_0x00420a40(iStack_10);
      puStack_2c = (undefined4 *)func_0x00428a40(*(int *)(iStack_10 + 0x2e) * 4 + 0x28);
      puStack_c = puStack_2c;
      if (puStack_2c != (undefined4 *)0x0) {
        *puStack_2c = 0x28;
        puStack_2c[1] = *(undefined4 *)(iStack_10 + 0x12);
        puStack_2c[2] = *(undefined4 *)(iStack_10 + 0x16);
        *(undefined2 *)(puStack_2c + 3) = 1;
        *(undefined2 *)((int)puStack_2c + 0xe) = *(undefined2 *)(iStack_10 + 0x1c);
        puStack_2c[4] = 0;
        puStack_2c[5] = 0;
        puStack_2c[6] = 0;
        puStack_2c[7] = 0;
        puStack_2c[8] = 0;
        puStack_2c[9] = 0;
        uStack_34 = (uint)*(ushort *)(iStack_10 + 0x1c);
        if ((uStack_34 == 4) || (uStack_34 == 8)) {
          puStack_24 = (undefined1 *)(iStack_10 + 0x36);
          puStack_18 = puStack_2c + 10;
          iStack_20 = *(int *)(iStack_10 + 0x2e) << 2;
          puStack_14 = puStack_24;
          for (iStack_28 = 0; iStack_28 != *(int *)(iStack_10 + 0x2e); iStack_28 = iStack_28 + 1) {
            if (iStack_28 == 0) {
              *puStack_24 = 0xff;
              puStack_24[1] = 0xff;
              puStack_24[2] = 0xff;
              puStack_24[3] = 0xff;
            }
            else {
              _memset(puStack_24 + iStack_28 * 4,0,4);
            }
          }
          func_0x0056d4d0(puStack_18,puStack_14,iStack_20);
        }
        (*API_USER32_DLL_GetDC)(0);
        uStack_1c = __chkesp();
        (*API_GDI32_DLL_CreateDIBSection)(uStack_1c,puStack_c,0,(int)puStack_8 + 4,0,0);
        uVar1 = __chkesp();
        *(undefined4 *)((int)puStack_8 + 0x14) = uVar1;
        (*API_GDI32_DLL_CreateCompatibleDC)(uStack_1c);
        uVar1 = __chkesp();
        *(undefined4 *)((int)puStack_8 + 0x10) = uVar1;
        (*API_USER32_DLL_ReleaseDC)(0,uStack_1c);
        __chkesp();
        puStack_14 = (undefined1 *)(iStack_10 + *(int *)(iStack_10 + 10));
        puStack_18 = *(undefined4 **)((int)puStack_8 + 4);
        uVar3 = puStack_c[1] & 0x80000003;
        if ((int)uVar3 < 0) {
          uVar3 = (uVar3 - 1 | 0xfffffffc) + 1;
        }
        if (uVar3 == 0) {
          iStack_20 = puStack_c[1];
        }
        else {
          iStack_20 = ((int)(puStack_c[1] + 4 + (puStack_c[1] + 4 >> 0x1f & 3U)) >> 2) << 2;
        }
        iStack_20 = iStack_20 * puStack_c[2];
        iStack_38 = *(ushort *)(iStack_10 + 0x1c) - 4;
        switch(*(ushort *)(iStack_10 + 0x1c)) {
        case 4:
          iStack_20 = iStack_20 / 2;
          break;
        case 8:
          break;
        case 0x10:
          iStack_20 = iStack_20 * 2;
          break;
        case 0x18:
          iStack_20 = iStack_20 * 3;
        }
        func_0x0056d4d0(puStack_18,puStack_14,iStack_20);
        puStack_30 = puStack_c;
        FUN_00428ad0(puStack_c);
      }
    }
  }
  puStack_8 = &UNK_0042051e;
  __chkesp();
  return;
}

