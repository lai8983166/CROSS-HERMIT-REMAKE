
void FUN__text__0041fe00(int param_1,int param_2)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_78 [16];
  int local_38;
  int local_34;
  uint local_30;
  int local_2c;
  int *local_28;
  undefined2 local_24;
  int *local_20;
  int local_1c;
  undefined4 local_18;
  int local_14;
  int *local_10;
  int local_c;
  int *local_8;
  
  puVar4 = local_78;
  for (iVar3 = 0x1d; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  FUN__text__0041fa50();
  local_c = param_1;
  iVar3 = FUN__text__004209f0(param_1);
  if (iVar3 == 0) {
    FUN__text__00420a40(local_c);
    local_2c = FUN__text__00428a40(*(int *)(local_c + 0x2e) * 4 + 0x28);
    *local_8 = local_2c;
    if (*local_8 != 0) {
      *(undefined4 *)*local_8 = 0x28;
      *(undefined4 *)(*local_8 + 4) = *(undefined4 *)(local_c + 0x12);
      *(undefined4 *)(*local_8 + 8) = *(undefined4 *)(local_c + 0x16);
      *(undefined2 *)(*local_8 + 0xc) = 1;
      *(undefined2 *)(*local_8 + 0xe) = *(undefined2 *)(local_c + 0x1c);
      *(undefined4 *)(*local_8 + 0x10) = 0;
      *(undefined4 *)(*local_8 + 0x14) = 0;
      *(undefined4 *)(*local_8 + 0x18) = 0;
      *(undefined4 *)(*local_8 + 0x1c) = 0;
      *(undefined4 *)(*local_8 + 0x20) = *(undefined4 *)(local_c + 0x2e);
      *(undefined4 *)(*local_8 + 0x24) = 0;
      local_30 = (uint)*(ushort *)(local_c + 0x1c);
      if ((local_30 == 4) || (local_30 == 8)) {
        local_10 = (int *)(local_c + 0x36);
        local_14 = *local_8 + 0x28;
        local_1c = *(int *)(local_c + 0x2e) << 2;
        if (param_2 != 0) {
          *(undefined1 *)local_10 = 0;
          *(undefined1 *)(local_c + 0x37) = 0;
          *(undefined1 *)(local_c + 0x38) = 0;
          *(undefined1 *)(local_c + 0x39) = 0;
          local_28 = local_10;
        }
        FUN__text__0056d4d0(local_14,local_10,local_1c);
      }
      (*API_USER32_DLL_GetDC)(0);
      local_18 = FUN__text__0056ce80();
      (*API_GDI32_DLL_CreateDIBSection)(local_18,*local_8,0,local_8 + 1,0,0);
      iVar3 = FUN__text__0056ce80();
      local_8[3] = iVar3;
      if ((local_8[3] == 0) &&
         (iVar3 = FUN__text__00424f80("hbmp!=0","e:\\crosshermit\\game\\src\\system\\dib.cpp",
                                      DAT_005ff5dc + 0x34,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_GDI32_DLL_CreateCompatibleDC)(local_18);
      iVar3 = FUN__text__0056ce80();
      local_8[2] = iVar3;
      if ((local_8[2] == 0) &&
         (iVar3 = FUN__text__00424f80("hdcbmp!=0","e:\\crosshermit\\game\\src\\system\\dib.cpp",
                                      DAT_005ff5dc + 0x36,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (*API_USER32_DLL_ReleaseDC)(0,local_18);
      FUN__text__0056ce80();
      local_10 = (int *)(local_c + *(int *)(local_c + 10));
      local_14 = local_8[1];
      uVar2 = *(uint *)(*local_8 + 4) & 0x80000003;
      if ((int)uVar2 < 0) {
        uVar2 = (uVar2 - 1 | 0xfffffffc) + 1;
      }
      if (uVar2 == 0) {
        local_1c = *(int *)(*local_8 + 4);
      }
      else {
        iVar3 = *(int *)(*local_8 + 4) + 4;
        local_1c = ((int)(iVar3 + (iVar3 >> 0x1f & 3U)) >> 2) << 2;
      }
      local_1c = local_1c * *(int *)(*local_8 + 8);
      local_34 = *(ushort *)(local_c + 0x1c) - 4;
      switch(*(ushort *)(local_c + 0x1c)) {
      case 4:
        local_1c = local_1c / 2;
        break;
      case 8:
        break;
      case 0x10:
        local_1c = local_1c * 2;
        break;
      case 0x18:
        local_1c = local_1c * 3;
      }
      FUN__text__0056d4d0(local_14,local_10,local_1c);
      local_8[6] = *(int *)(*local_8 + 4);
      local_8[7] = *(int *)(*local_8 + 8);
      local_8[8] = (uint)*(ushort *)(local_c + 0x1c);
      local_38 = *(ushort *)(local_c + 0x1c) - 4;
      switch(*(ushort *)(local_c + 0x1c)) {
      case 4:
      case 8:
        local_20 = (int *)(local_c + 0x36);
        local_8[9] = *local_20;
        break;
      case 0x10:
        local_24 = (undefined2)*local_10;
        break;
      case 0x18:
        local_20 = local_10;
        local_8[9] = *local_10;
      }
    }
  }
  local_8 = (int *)0x4201b3;
  FUN__text__0056ce80();
  return;
}

