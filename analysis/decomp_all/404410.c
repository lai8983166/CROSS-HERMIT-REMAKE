
void __thiscall FUN__text__00404410(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_70 [16];
  int local_30;
  int local_2c;
  int local_28;
  uint local_24;
  int local_20;
  int local_1c;
  char *local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(int *)(param_1 + 0x2c) != 0) {
    local_14 = param_2;
    local_18 = (char *)(param_2 + 0x36);
    local_2c = param_2 + *(int *)(param_2 + 10);
    local_8 = param_1;
    if ((*(short *)(param_1 + 0x3c) < *(short *)(param_2 + 0x12)) &&
       (iVar2 = FUN__text__00424f80("imgtw >= (sint16)bmp_head->data_hd.screen_x",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff094 + 0xe,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((*(short *)(local_8 + 0x3e) < *(short *)(local_14 + 0x16)) &&
       (iVar2 = FUN__text__00424f80("imgth >= (sint16)bmp_head->data_hd.screen_y",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff094 + 0xf,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    uVar3 = (int)*(short *)(local_8 + 0x38) & 0x80000003;
    if ((int)uVar3 < 0) {
      uVar3 = (uVar3 - 1 | 0xfffffffc) + 1;
    }
    if (uVar3 == 0) {
      local_28 = (int)*(short *)(local_8 + 0x38);
    }
    else {
      iVar2 = *(short *)(local_8 + 0x38) + 4;
      local_28 = ((int)(iVar2 + (iVar2 >> 0x1f & 3U)) >> 2) << 2;
    }
    if (*(short *)(local_8 + 0x38) == 1) {
      local_28 = 1;
    }
    iVar2 = FUN__text__00403910(&local_10);
    if (iVar2 == 0) {
      for (local_20 = 0; local_20 != *(short *)(local_8 + 0x3a); local_20 = local_20 + 1) {
        local_30 = local_c + local_10 * local_20;
        for (local_1c = 0; local_1c != local_28; local_1c = local_1c + 1) {
          local_24 = (uint)*(byte *)(local_2c +
                                    ((*(short *)(local_8 + 0x3a) - local_20) + -1) * local_28 +
                                    local_1c);
          if ((((param_3 == 1) && (local_18[2] == local_18[local_24 * 4 + 2])) &&
              (local_18[1] == local_18[local_24 * 4 + 1])) && (*local_18 == local_18[local_24 * 4]))
          {
            *(undefined2 *)(local_30 + local_1c * 2) = 0;
          }
          else {
            *(ushort *)(local_30 + local_1c * 2) =
                 (ushort)(((int)(uint)(byte)local_18[local_24 * 4 + 2] >> 3) << 0xb) |
                 (ushort)(((int)(uint)(byte)local_18[local_24 * 4 + 1] >> 2) << 5) |
                 (ushort)((int)(uint)(byte)local_18[local_24 * 4] >> 3);
          }
        }
      }
      iVar2 = FUN__text__00403990();
      if (iVar2 == 0) {
        FUN__text__00403aa0(0);
      }
    }
  }
  local_8 = 0x404684;
  FUN__text__0056ce80();
  return;
}

