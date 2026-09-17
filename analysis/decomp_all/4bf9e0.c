
void __fastcall FUN__text__004bf9e0(int param_1)

{
  int iVar1;
  int iVar2;
  short sVar3;
  undefined2 extraout_var;
  undefined4 *puVar4;
  undefined4 local_7c [16];
  short local_3c;
  short local_38;
  undefined2 local_34;
  undefined2 local_30 [6];
  short local_24;
  ushort local_20;
  ushort local_1c;
  undefined *local_18;
  undefined *local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar4 = local_7c;
  for (iVar2 = 0x1e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c < *(short *)(local_8 + 0x12a2); local_c = local_c + 1) {
    for (local_10 = 0; local_10 < *(short *)(local_8 + 0x12a2); local_10 = local_10 + 1) {
      if (local_c != local_10) {
        iVar2 = *(short *)(local_8 + 0x11da + local_c * 2) * 0x4a0;
        local_14 = &DAT_007e17e8 + iVar2;
        iVar1 = *(short *)(local_8 + 0x11da + local_10 * 2) * 0x4a0;
        local_18 = &DAT_007e17e8 + iVar1;
        local_1c = (ushort)(byte)(&DAT_006b2d8a)[*(short *)(&DAT_007e17ee + iVar2) * 0x40];
        local_20 = (ushort)(byte)(&DAT_006b2d8a)[*(short *)(&DAT_007e17ee + iVar1) * 0x40];
        if ((ushort)(byte)(&DAT_006b2d8a)[*(short *)(&DAT_007e17ee + iVar2) * 0x40] ==
            (ushort)(byte)(&DAT_006b2d8a)[*(short *)(&DAT_007e17ee + iVar1) * 0x40]) {
          FUN__text__004d3960(*(undefined2 *)(local_8 + 0x11da + local_c * 2),
                              *(undefined2 *)(local_8 + 0x11da + local_10 * 2),1);
        }
        if (local_14[0x50] == local_18[0x50]) {
          FUN__text__004d3960(*(undefined2 *)(local_8 + 0x11da + local_c * 2),
                              *(undefined2 *)(local_8 + 0x11da + local_10 * 2),1);
        }
      }
    }
  }
  for (local_c = 0; local_c < *(short *)(local_8 + 0x12a2); local_c = local_c + 1) {
    for (local_10 = 0; local_10 < *(short *)(local_8 + 0x12a2); local_10 = local_10 + 1) {
      if (local_c != local_10) {
        FUN__text__004d3960(CONCAT22(local_10 >> 0xf,*(undefined2 *)(local_8 + 0x11da + local_c * 2)
                                    ),
                            CONCAT22(local_10 >> 0xf,
                                     *(undefined2 *)(local_8 + 0x11da + local_10 * 2)),2);
      }
    }
  }
  for (local_c = 0; local_c < *(short *)(local_8 + 0x12a2); local_c = local_c + 1) {
    for (local_10 = 0; local_10 < *(short *)(local_8 + 0x11ce); local_10 = local_10 + 1) {
      sVar3 = *(short *)(local_8 + 0x116a + local_10 * 2);
      if (*(short *)(local_8 + 0x11da + local_c * 2) != sVar3) {
        sVar3 = sVar3 >> 0xf;
        FUN__text__004d3960(CONCAT22(sVar3,*(undefined2 *)(local_8 + 0x11da + local_c * 2)),
                            CONCAT22(sVar3,*(undefined2 *)(local_8 + 0x116a + local_10 * 2)),
                            0xffffffff);
      }
    }
  }
  for (local_24 = 0; local_24 < 5; local_24 = local_24 + 1) {
    for (local_c = 0; local_c < *(short *)(local_8 + 0x1160 + local_24 * 2); local_c = local_c + 1)
    {
      for (local_10 = 0; local_10 < *(short *)(local_8 + 0x1160 + local_24 * 2);
          local_10 = local_10 + 1) {
        if (local_c != local_10) {
          FUN__text__004d3960(*(undefined2 *)(local_8 + 0x1138 + local_24 * 8 + local_c * 2),
                              *(undefined2 *)(local_8 + 0x1138 + local_24 * 8 + local_10 * 2),1);
        }
      }
    }
    for (local_c = 0; sVar3 = *(short *)(local_8 + 0x1160 + local_24 * 2), local_c < sVar3;
        local_c = local_c + 1) {
      FUN__text__004d3960(*(undefined2 *)(local_8 + 0x1138 + local_24 * 8 + local_c * 2),
                          CONCAT22(sVar3 >> 0xf,*(undefined2 *)(local_8 + 0x11d0 + local_24 * 2)),1)
      ;
      FUN__text__004d3960(*(undefined2 *)(local_8 + 0x11d0 + local_24 * 2),
                          *(undefined2 *)(local_8 + 0x1138 + local_24 * 8 + local_c * 2),1);
    }
  }
  local_30[0] = 3;
  local_30[1] = 2;
  local_30[2] = 1;
  local_30[3] = 0;
  local_30[4] = 0xffff;
  for (local_c = 0; local_c < DAT_007a5298; local_c = local_c + 1) {
    local_34 = local_30[*(short *)(&DAT_007a5306 + local_c * 0x70)];
    for (local_38 = 0; local_38 < *(short *)(&DAT_007a52f8 + local_c * 0x70);
        local_38 = local_38 + 1) {
      for (local_3c = 0; local_3c < *(short *)(&DAT_007a52f8 + local_c * 0x70);
          local_3c = local_3c + 1) {
        if (local_38 != local_3c) {
          sVar3 = *(short *)(&DAT_007a52f8 + local_c * 0x70) >> 0xf;
          FUN__text__004d3960(CONCAT22(sVar3,*(undefined2 *)
                                              (&DAT_007a52d0 + local_38 * 2 + local_c * 0x70)),
                              CONCAT22(sVar3,*(undefined2 *)
                                              (&DAT_007a52d0 + local_3c * 2 + local_c * 0x70)),
                              CONCAT22(sVar3,local_34));
        }
      }
    }
    for (local_38 = 0; local_38 < *(short *)(&DAT_007a52f8 + local_c * 0x70);
        local_38 = local_38 + 1) {
      for (local_3c = 0; local_3c < *(short *)(&DAT_007a5304 + local_c * 0x70);
          local_3c = local_3c + 1) {
        sVar3 = local_3c >> 0xf;
        FUN__text__004d3960(CONCAT22(sVar3,*(undefined2 *)
                                            (&DAT_007a52d0 + local_38 * 2 + local_c * 0x70)),
                            CONCAT22(sVar3,*(undefined2 *)
                                            (&DAT_007a52fa + local_3c * 2 + local_c * 0x70)),
                            CONCAT22(sVar3,local_34));
        FUN__text__004d3960(CONCAT22(extraout_var,
                                     *(undefined2 *)(&DAT_007a52fa + local_3c * 2 + local_c * 0x70))
                            ,CONCAT22(extraout_var,
                                      *(undefined2 *)(&DAT_007a52d0 + local_38 * 2 + local_c * 0x70)
                                     ),CONCAT22(extraout_var,local_34));
      }
    }
  }
  local_8 = 0x4bffb7;
  FUN__text__0056ce80();
  return;
}

