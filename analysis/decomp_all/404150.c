
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN__text__00404150(int param_1,int param_2,int param_3,undefined4 param_4,char *param_5)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_74 [16];
  int local_34;
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
  
  puVar4 = local_74;
  for (iVar3 = 0x1c; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if ((*(int *)(param_1 + 0x2c) != 0) &&
     (local_8 = param_1, iVar3 = FUN__text__00403910(&local_10), iVar3 == 0)) {
    local_14 = param_2;
    if (param_5 == (char *)0x0) {
      local_18 = (char *)(param_2 + 0x36);
    }
    else {
      local_18 = param_5;
    }
    local_2c = param_2 + *(int *)(param_2 + 10);
    if ((*(short *)(local_8 + 0x3c) < *(short *)(param_2 + 0x12)) &&
       (iVar3 = FUN__text__00424f80("imgtw >= (sint16)bmp_head->data_hd.screen_x",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff090 + 0x12,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((*(short *)(local_8 + 0x3e) < *(short *)(local_14 + 0x16)) &&
       (iVar3 = FUN__text__00424f80("imgth >= (sint16)bmp_head->data_hd.screen_y",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff090 + 0x13,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    uVar2 = (int)*(short *)(local_8 + 0x38) & 0x80000003;
    if ((int)uVar2 < 0) {
      uVar2 = (uVar2 - 1 | 0xfffffffc) + 1;
    }
    if (uVar2 == 0) {
      local_28 = (int)*(short *)(local_8 + 0x38);
    }
    else {
      iVar3 = *(short *)(local_8 + 0x38) + 4;
      local_28 = ((int)(iVar3 + (iVar3 >> 0x1f & 3U)) >> 2) << 2;
    }
    if (*(short *)(local_8 + 0x38) == 1) {
      local_28 = 1;
    }
    for (local_34 = 1; local_34 != 0x100; local_34 = local_34 + 1) {
      if ((((param_3 == 1) && (local_18[2] == local_18[local_34 * 4 + 2])) &&
          (local_18[1] == local_18[local_34 * 4 + 1])) && (*local_18 == local_18[local_34 * 4])) {
        *(undefined2 *)(&DAT_00765520 + local_34 * 2) = 0;
      }
      else {
        *(ushort *)(&DAT_00765520 + local_34 * 2) =
             (ushort)(((int)(uint)(byte)local_18[local_34 * 4 + 2] >> 3) << 10) |
             (ushort)(((int)(uint)(byte)local_18[local_34 * 4 + 1] >> 3) << 5) |
             (ushort)((int)(uint)(byte)local_18[local_34 * 4] >> 3) | 0x8000;
      }
    }
    _DAT_00765520 = 0;
    for (local_20 = 0; local_20 != *(short *)(local_8 + 0x3a); local_20 = local_20 + 1) {
      local_30 = local_c + local_10 * local_20;
      for (local_1c = 0; local_1c != local_28; local_1c = local_1c + 1) {
        local_24 = (uint)*(byte *)(local_2c +
                                  ((*(short *)(local_8 + 0x3a) - local_20) + -1) * local_28 +
                                  local_1c);
        *(undefined2 *)(local_30 + local_1c * 2) = *(undefined2 *)(&DAT_00765520 + local_24 * 2);
      }
    }
    iVar3 = FUN__text__00403990();
    if (iVar3 == 0) {
      FUN__text__00403aa0(0);
    }
  }
  local_8 = 0x404407;
  FUN__text__0056ce80();
  return;
}

