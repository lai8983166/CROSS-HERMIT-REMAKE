
void FUN__text__00494a50(int param_1)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_80 [16];
  uint local_40;
  uint local_3c;
  uint local_38;
  uint local_34;
  uint local_30;
  int local_2c;
  int local_28;
  int local_24;
  uint local_20;
  uint local_1c;
  undefined4 local_18;
  int local_14;
  undefined *local_10;
  int *local_c;
  int local_8;
  
  puVar3 = local_80;
  for (iVar1 = 0x1f; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar1 = FUN__text__00468d10(param_1);
  if (((iVar1 != 0) && (iVar1 = FUN__text__00469480(param_1), iVar1 != 0)) &&
     (iVar1 = FUN__text__0046a4c0(param_1), iVar1 != 0)) {
    iVar1 = (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40;
    local_10 = &DAT_006b2d88 + iVar1;
    local_1c = (uint)(byte)(&DAT_006b2d8a)[iVar1];
    for (local_14 = 0; local_14 != *(int *)(local_8 + 0x108b50); local_14 = local_14 + 1) {
      *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_14 * 4) + 0x28c) = 0;
    }
    local_c = (int *)(local_8 + 0xdc8ec);
    local_18 = 0;
    for (local_14 = 0; local_14 != *local_c; local_14 = local_14 + 1) {
      iVar1 = FUN__text__00468d10(local_c[local_14 + 1]);
      if (((iVar1 != 0) && (iVar1 = FUN__text__00469480(local_c[local_14 + 1]), iVar1 != 0)) &&
         (iVar1 = FUN__text__0046a4c0(local_c[local_14 + 1]), iVar1 != 0)) {
        local_28._0_2_ = (short)((uint)*(int *)(local_c[local_14 + 1] + 0x2f0) >> 0x10);
        iVar1 = (int)(short)local_28;
        local_24._0_2_ = (short)((uint)*(int *)(local_c[local_14 + 1] + 0x2ec) >> 0x10);
        iVar2 = (int)(short)local_24;
        local_28 = *(int *)(local_c[local_14 + 1] + 0x2f0) >> 0x10;
        local_24 = *(int *)(local_c[local_14 + 1] + 0x2ec) >> 0x10;
        iVar1 = FUN__text__0046b1a0(iVar2 - *(short *)(local_8 + 0x2a30e),
                                    (iVar1 - *(short *)(local_8 + 0x2a310)) + 0x1e);
        if (iVar1 != 0) {
          local_20 = (uint)(byte)(&DAT_006b2d8a)
                                 [(uint)*(ushort *)(*(int *)(local_c[local_14 + 1] + 600) + 0xc) *
                                  0x40];
          local_2c = local_1c - 2;
          switch(local_2c) {
          case 0:
            local_34 = local_20;
            if (local_20 == 2) {
LAB__text__00494c94:
              *(undefined1 *)(local_c[local_14 + 1] + 0x28c) = 1;
              local_18 = 1;
            }
            break;
          case 1:
            local_38 = local_20;
            if (local_20 == 3) goto LAB__text__00494c94;
            break;
          case 2:
            local_3c = local_20;
            if (local_20 == 4) goto LAB__text__00494c94;
            break;
          case 3:
            local_40 = local_20;
            if (local_20 == 5) goto LAB__text__00494c94;
            break;
          default:
            local_30 = local_20;
            if ((local_20 < 2) || (5 < local_20)) goto LAB__text__00494c94;
          }
        }
      }
    }
    FUN__text__0046f170();
  }
  local_8 = 0x494ccb;
  FUN__text__0056ce80();
  return;
}

