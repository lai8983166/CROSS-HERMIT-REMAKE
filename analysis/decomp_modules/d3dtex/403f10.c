
void __thiscall FUN__text__00403f10(int param_1,int param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if ((*(int *)(param_1 + 0x2c) != 0) &&
     (local_8 = param_1, iVar2 = FUN__text__00403910(&local_10), iVar2 == 0)) {
    local_14 = param_2;
    local_20 = param_2 + *(int *)(param_2 + 10);
    if ((*(short *)(local_8 + 0x3c) < *(short *)(param_2 + 0x12)) &&
       (iVar2 = FUN__text__00424f80("imgtw >= (sint16)bmp_head->data_hd.screen_x",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff08c + 0xd,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((*(short *)(local_8 + 0x3e) < *(short *)(local_14 + 0x16)) &&
       (iVar2 = FUN__text__00424f80("imgth >= (sint16)bmp_head->data_hd.screen_y",
                                    "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                    DAT_005ff08c + 0xe,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    uVar3 = (int)*(short *)(local_8 + 0x38) & 0x80000003;
    if ((int)uVar3 < 0) {
      uVar3 = (uVar3 - 1 | 0xfffffffc) + 1;
    }
    if (uVar3 == 0) {
      local_1c = (int)*(short *)(local_8 + 0x38);
    }
    else {
      iVar2 = *(short *)(local_8 + 0x38) + 4;
      local_1c = ((int)(iVar2 + (iVar2 >> 0x1f & 3U)) >> 2) << 2;
    }
    if (*(short *)(local_8 + 0x38) == 1) {
      local_1c = 1;
    }
    if (param_4 != 0) {
      iVar2 = FUN__text__00403af0(local_14,param_3,1);
      if (iVar2 != 0) goto LAB__text__004040eb;
      *(ushort *)(local_8 + 0x44) = *(ushort *)(local_8 + 0x44) | 1;
    }
    iVar2 = FUN__text__00403910(&local_10);
    if (iVar2 == 0) {
      for (local_18 = 0; local_18 != *(short *)(local_8 + 0x3a); local_18 = local_18 + 1) {
        local_24 = local_c + local_10 * local_18;
        FUN__text__0056d4d0(local_24,local_20 +
                                     ((*(short *)(local_8 + 0x3a) - local_18) + -1) * local_1c,
                            local_1c);
      }
      iVar2 = FUN__text__00403990();
      if (iVar2 == 0) {
        FUN__text__00403aa0(0);
      }
    }
  }
LAB__text__004040eb:
  local_8 = 0x4040f8;
  FUN__text__0056ce80();
  return;
}

