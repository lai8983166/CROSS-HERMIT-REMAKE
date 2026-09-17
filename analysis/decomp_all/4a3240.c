
void FUN__text__004a3240(void)

{
  uint uVar1;
  bool bVar2;
  ushort uVar3;
  int iVar4;
  undefined2 uVar5;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  ushort uVar6;
  undefined4 *puVar7;
  undefined4 local_168 [16];
  uint local_128;
  char local_124;
  char local_120;
  short local_11c [2];
  undefined2 local_118;
  undefined2 local_10c;
  undefined2 local_108;
  short local_104;
  short local_100;
  int local_fc;
  ushort local_f8;
  int local_f4 [8];
  undefined2 local_d4;
  undefined2 local_d0;
  short local_cc;
  short local_c8;
  short local_c4;
  short local_c0;
  undefined2 local_be;
  undefined1 local_b0 [28];
  short local_94;
  undefined4 local_90;
  undefined4 local_8c;
  undefined2 local_88;
  undefined4 local_84;
  short local_80;
  uint local_7c;
  undefined2 local_78;
  undefined2 local_74;
  undefined1 local_70;
  short local_6c;
  short local_68;
  undefined2 local_64;
  short local_60;
  short local_5c;
  short local_58;
  undefined *local_54;
  short local_50;
  short local_4c;
  short local_48;
  undefined2 local_44;
  short local_40;
  short local_3c;
  short local_38;
  short local_34;
  short local_30;
  short local_2c;
  short local_28;
  undefined *local_24;
  undefined1 local_20 [12];
  uint local_14;
  short local_10;
  undefined4 local_c;
  int local_8;
  
  puVar7 = local_168;
  for (iVar4 = 0x59; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar7 = 0xcccccccc;
    puVar7 = puVar7 + 1;
  }
  local_10 = 0;
  if (DAT_007d57c6 != 0) {
    FUN__text__004d5ec0(local_20,DAT_007d57d0,CONCAT22(DAT_007d57c6 >> 0xf,DAT_007d57d2),
                        DAT_007d57d4,DAT_007d57d6);
    if ((local_14 & 0xffff) == 0) {
      DAT_007d57c6 = 0;
    }
    else {
      local_24 = &DAT_007e17e8 + DAT_007d57c8 * 0x4a0;
      local_28 = DAT_007d57cc;
      local_2c = DAT_007d57ce;
      local_30 = DAT_007d57cc + 0xcc;
      local_34 = (short)(DAT_007d57ce + 0x28);
      local_38 = (short)(DAT_007d57cc + 0x59);
      local_3c = DAT_007d57ce + 5;
      FUN__text__004d2700(&DAT_0061b4e8,1,0x6f,
                          CONCAT22((short)((uint)(DAT_007d57cc + 0x59) >> 0x10),DAT_007d57cc),
                          CONCAT22((short)((uint)(DAT_007d57ce + 0x28) >> 0x10),DAT_007d57ce));
      local_40 = (short)((*(short *)(local_24 + 6) + -1) / 10) * 0x52;
      iVar4 = ((*(short *)(local_24 + 6) + -1) % 10) * 0x18 + 0xbc;
      local_44 = (undefined2)iVar4;
      FUN__text__004d2830(&DAT_0061b518,1,0x6c,CONCAT22((short)((uint)iVar4 >> 0x10),local_38),
                          local_3c,CONCAT22((short)((uint)((*(short *)(local_24 + 6) + -1) / 10) >>
                                                   0x10),local_40),iVar4,0x52,0x18);
      FUN__text__004d1ec0(local_38 + 0x6e,local_3c + 6,0,0,2,0x6e,local_24[0x50],10,1,0,5,0,
                          &DAT_0061b548);
      local_48 = (DAT_007a528e + -4) * 5 + DAT_007a5290 + -1;
      local_4c = 0;
      local_50 = 0;
      local_54 = &DAT_007cf34c + DAT_007d57c8 * 0x124;
      local_58 = 0;
      local_5c = 0;
      local_c = (uint)local_c._2_2_ << 0x10;
      while ((int)(local_c & 0xffff) < (int)local_48) {
        local_120 = (&UNK_007cf370)[(local_c & 0xffff) * 3 + DAT_007d57c8 * 0x124];
        if (local_120 == '\x01') {
          local_58 = local_58 + 1;
        }
        else if (local_120 == '\x02') {
          local_5c = local_5c + 1;
        }
        local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
      }
      FUN__text__004d1ec0(local_38 + 0x15e,local_3c + 0x91,0,0,2,0x6e,(int)local_5c,10,1,0,5,0,
                          &DAT_0061b558);
      FUN__text__004d1ec0(local_38 + 0x15e,local_3c + 0xa3,0,0,2,0x6e,(int)local_58,10,1,0,5,0,
                          &DAT_0061b558);
      if (local_48 < 5) {
        local_4c = local_48;
      }
      else {
        local_4c = 5;
      }
      local_c = local_c & 0xffff0000;
      while( true ) {
        if ((int)local_4c <= (int)(local_c & 0xffff)) break;
        local_50 = (local_48 - (short)local_c) + -1;
        local_60 = local_28 + 0x155;
        iVar4 = local_2c + 0x23 + (local_c & 0xffff) * 0x16;
        local_64 = (undefined2)iVar4;
        uVar5 = (undefined2)((uint)iVar4 >> 0x10);
        local_68 = (short)(char)local_54[local_50 * 3 + 0x25];
        local_6c = (short)(char)local_54[local_50 * 3 + 0x26];
        local_70 = 0xff;
        local_74 = 0;
        local_124 = local_54[local_50 * 3 + 0x24];
        uVar6 = (ushort)((uint)(local_50 * 3) >> 0x10);
        uVar3 = (ushort)((uint)local_54 >> 0x10);
        if (local_124 == '\x01') {
          FUN__text__004aa6c0(CONCAT22(uVar5,local_60),CONCAT22(uVar3,local_64),
                              CONCAT22(uVar6,local_68),CONCAT22(uVar5,local_6c),0xff,
                              (uint)uVar6 << 0x10);
        }
        else if (local_124 == '\x02') {
          FUN__text__004aa7e0(CONCAT22(uVar6,local_60),iVar4,CONCAT22(uVar3,local_68),
                              CONCAT22(uVar6,local_6c),1,0,
                              CONCAT31((int3)(CONCAT22(uVar5,local_6c) >> 8),0xff),
                              (uint)uVar3 << 0x10);
        }
        else if (local_124 == '\x03') {
          local_78 = 0x37;
          FUN__text__004d2700(&DAT_0061b578,1,0,CONCAT22(uVar6,local_60),iVar4);
        }
        local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
      }
      local_80 = FUN__text__004d45c0(DAT_007d57c8);
      local_84 = (uint)local_84._2_2_ << 0x10;
      local_8c = (uint)local_8c._2_2_ << 0x10;
      local_90 = 0;
      local_c = local_c & 0xffff0000;
      uVar5 = extraout_var;
      while ((local_c & 0xffff) < 8) {
        local_7c = CONCAT22(local_7c._2_2_,
                            *(undefined2 *)
                             (local_8 + 0x76ca + local_80 * 0x10 + (local_c & 0xffff) * 2));
        uVar1 = local_84 >> 0x10;
        local_84 = local_84 & 0xffff0000;
        local_128 = local_c & 0xffff;
        if (local_128 < 7) {
          FUN__text__004d56a0(local_b0,CONCAT22((short)((uint)*(undefined4 *)
                                                               (local_24 +
                                                               (local_c & 0xffff) * 8 + 0x10) >>
                                                       0x10),
                                                (ushort)(byte)local_24[(local_c & 0xffff) * 8 + 0xc]
                                               ),
                              *(undefined4 *)(local_24 + (local_c & 0xffff) * 8 + 0x10));
          local_88 = (undefined2)((local_94 * 0x44) / 100);
          FUN__text__004d2830(&DAT_0061b508,1,0x6e,local_28 + 0x65,
                              local_2c + 0x35 + (local_c & 0xffff) * 0x12,0xf6,0x10c,
                              CONCAT22((short)((uint)((local_94 * 0x44) % 100) >> 0x10),local_88),1)
          ;
          uVar3 = (ushort)(byte)local_24[(local_c & 0xffff) * 8 + 0xc];
          local_84 = CONCAT22(local_84._2_2_,uVar3);
          local_8c = CONCAT22(local_8c._2_2_,(short)local_8c + uVar3);
          local_88 = (undefined2)((ulonglong)((uint)uVar3 * 0x44) / 0x87);
        }
        else if (local_128 == 7) {
          local_84 = CONCAT22((short)uVar1,(short)local_8c);
          local_88 = (undefined2)((ulonglong)((local_8c & 0xffff) * 0x44) / 0x3b1);
        }
        FUN__text__004d2830(&DAT_0061b4f8,1,0x6e,local_28 + 0x65,
                            local_2c + 0x29 + (local_c & 0xffff) * 0x12,0xf6,
                            (local_c & 0xffff) * 10 + 0xbc,local_88,10);
        FUN__text__004d1ec0(local_30,(int)local_34 + (local_c & 0xffff) * 0x12,0,0,3,0x6e,
                            local_84 & 0xffff,10,1,0,5,0,&DAT_0061b538);
        FUN__text__004d1ec0(local_30 + 0x24,(int)local_34 + (local_c & 0xffff) * 0x12,0,0,2,0x6e,
                            local_7c & 0xffff,10,1,0,5,0,&DAT_0061b548);
        uVar5 = extraout_var_00;
        local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
      }
      if ((DAT_007d57ca != -1) &&
         (FUN__text__004a95f0(&local_c0,CONCAT22(uVar5,DAT_007d57ca)), local_c0 == 4)) {
        local_cc = DAT_007d57c8;
        local_d0 = *(undefined2 *)(&DAT_007aaa1c + DAT_007d57ca * 0x1c);
        local_d4 = local_be;
        FUN__text__004d3600(local_f4,CONCAT22(extraout_var_01,DAT_007d57c8),local_d0,
                            CONCAT22((short)((uint)(DAT_007d57ca * 0x1c) >> 0x10),local_be));
        local_10 = 0;
        for (local_c4 = 0; local_c4 < 7; local_c4 = local_c4 + 1) {
          local_f8 = 0;
          local_fc = *(int *)(local_24 + local_c4 * 8 + 0x10) + local_f4[local_c4];
          local_100 = FUN__text__004d5600(local_fc);
          local_104 = local_100 - (ushort)(byte)local_24[local_c4 * 8 + 0xc];
          local_10 = local_10 + local_104;
          bVar2 = 7 < local_104;
          if (bVar2) {
            local_104 = 7;
          }
          local_f8 = (ushort)bVar2;
          iVar4 = local_2c + 0x29 + local_c4 * 0x12;
          local_108 = (undefined2)iVar4;
          if (local_f4[local_c4] != 0) {
            if (local_104 == 0) {
              FUN__text__004d2700(&DAT_0061b588,1,0x6e,local_28 + 0x104,iVar4);
            }
            else {
              for (local_c8 = 0; local_c8 < local_104; local_c8 = local_c8 + 1) {
                iVar4 = local_c8 * 10;
                uVar1 = local_28 + 0x104 + iVar4;
                local_10c = (undefined2)uVar1;
                if ((local_c8 == 6) && (iVar4 = 0, local_f8 != 0)) {
                  FUN__text__004d2790(&DAT_0061b598,1,0x6e,uVar1 & 0xffff,
                                      CONCAT22((short)(uVar1 >> 0x10),local_108),0x14,0);
                }
                else {
                  FUN__text__004d2790(&DAT_0061b598,1,0x6e,uVar1,
                                      CONCAT22((short)((uint)iVar4 >> 0x10),local_108),10,0);
                }
              }
            }
          }
        }
      }
      if (DAT_007d57ca != -1) {
        FUN__text__004a95f0(local_11c,DAT_007d57ca);
        if ((local_11c[0] == 4) && (DAT_007d57c4 == 0)) {
          DAT_007d57c4 = 1;
          FUN__text__004d48a0(DAT_007d57c8,4,0xffffffff,CONCAT22(extraout_var_02,local_10));
        }
        if ((local_11c[0] == 2) && (DAT_007d57c4 == 0)) {
          DAT_007d57c4 = 1;
          FUN__text__004d48a0(DAT_007d57c8,3,0xffffffff,local_118);
        }
      }
    }
  }
  local_8 = 0x4a3c99;
  FUN__text__0056ce80();
  return;
}

