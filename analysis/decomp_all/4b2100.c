
void __fastcall FUN__text__004b2100(int param_1)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_a4 [16];
  int local_64;
  byte local_60;
  undefined3 uStack_5f;
  ushort local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined2 local_50;
  short local_4c;
  uint local_48;
  uint local_44;
  undefined *local_40;
  undefined *local_3c;
  ushort local_38;
  undefined2 uStack_36;
  ushort local_34 [18];
  undefined *local_10;
  undefined4 local_c;
  int local_8;
  
  iVar3 = 0x28;
  puVar4 = local_a4;
  while( true ) {
    if (iVar3 == 0) break;
    iVar3 = iVar3 + -1;
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  local_34[0] = 0;
  local_34[1] = 0;
  local_34[2] = 0x152;
  local_34[3] = 0x41;
  local_34[4] = 300;
  local_34[5] = 0x67;
  local_34[6] = 0x106;
  local_34[7] = 0x8d;
  local_34[8] = 0xe0;
  local_34[9] = 0xb3;
  local_34[10] = 0xba;
  local_34[0xb] = 0xd9;
  local_34[0xc] = 0x94;
  local_34[0xd] = 0xff;
  local_34[0xe] = 0x6e;
  local_34[0xf] = 0x125;
  local_34[0x10] = 0x2b;
  local_34[0x11] = 0x168;
  uVar2 = (ushort)*(char *)(param_1 + 0x570);
  _local_38 = CONCAT22(uStack_36,uVar2);
  local_10 = &DAT_0061bf40;
  if (uVar2 != 0) {
    FUN__text__004d2830(&DAT_0061bf40,1,0x4d,0x33d,CONCAT22(0x61,local_34[(uint)uVar2 * 2]),
                        CONCAT22(0x61,DAT_0061bf44),CONCAT22(0x61,DAT_0061bf46),
                        CONCAT22((short)((uint)uVar2 * 2 >> 0x10),DAT_0061bf48),
                        local_34[(uint)uVar2 * 2 + 1]);
  }
  local_3c = &DAT_006b2d88 + (uint)*(ushort *)(local_8 + 0x632) * 0x40;
  local_40 = &DAT_007e17e8 + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x4a0;
  local_44 = CONCAT22(local_44._2_2_,(short)*(char *)(local_8 + 0x582));
  local_48 = CONCAT22(local_48._2_2_,(short)*(char *)(local_8 + 0x570));
  local_4c = 0;
  local_50 = 1;
  local_54 = (uint)local_54._2_2_ << 0x10;
  local_58 = (uint)local_58._2_2_ << 0x10;
  local_c = (uint)local_c._2_2_ << 0x10;
  while ((local_c & 0xffff) < (local_48 & 0xffff)) {
    local_4c = (short)local_44 + (short)local_c;
    if (*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) != 0) {
      FUN__text__004b4b00(0x341,local_34[(local_44 & 0xffff) * 2 + 1] + 0x47 +
                                (local_c & 0xffff) * 0x26,
                          *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) + -1,1,0x3f);
      *(undefined2 *)(&DAT_007d6ada + (local_c & 0xffff) * 0x80) = 0x3d;
      FUN__text__00408f90((0x78 - *(short *)(&DAT_007d6aa4 + (local_c & 0xffff) * 0x80)) / 2 + 0x369
                          ,local_34[(local_44 & 0xffff) * 2 + 1] + 0x49 + (local_c & 0xffff) * 0x26)
      ;
      local_54 = local_54 & 0xffff0000;
      local_58 = local_58 & 0xffff0000;
      while ((local_58 & 0xffff) < 3) {
        local_5c = 0xffff;
        bVar1 = (&DAT_006d514d)
                [(local_58 & 0xffff) + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
        _local_60 = CONCAT31(uStack_5f,bVar1);
        local_64 = bVar1 - 8;
        switch(local_64) {
        case 0:
          local_5c = *(ushort *)
                      (&DAT_006d5124 + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 1:
          local_5c = *(ushort *)
                      (&DAT_006d5126 + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 2:
          local_5c = *(ushort *)
                      (&DAT_006d5128 + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 3:
          local_5c = *(ushort *)
                      (&DAT_006d512a + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 4:
          local_5c = *(ushort *)
                      (&DAT_006d512c + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 5:
          local_5c = *(ushort *)
                      (&DAT_006d512e + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 6:
          local_5c = (ushort)(byte)(&DAT_006d5130)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 7:
          local_5c = *(ushort *)
                      (&DAT_006d5132 + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 8:
          local_5c = (ushort)(byte)(&DAT_006d5134)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 9:
          local_5c = (ushort)(byte)(&DAT_006d5135)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 10:
          local_5c = (ushort)(byte)(&DAT_006d5136)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 0xb:
          local_5c = (ushort)(byte)(&DAT_006d5137)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 0xc:
          local_5c = (ushort)(byte)(&DAT_006d5138)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 0xd:
          local_5c = (ushort)(byte)(&DAT_006d5139)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 0xe:
          local_5c = *(ushort *)
                      (&DAT_006d513a + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 0xf:
          local_5c = *(ushort *)
                      (&DAT_006d513c + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 0x10:
          local_5c = *(ushort *)
                      (&DAT_006d513e + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 0x11:
          local_5c = (ushort)(byte)(&DAT_006d5140)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
          break;
        case 0x12:
          local_5c = *(ushort *)
                      (&DAT_006d5144 + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 0x13:
          local_5c = *(ushort *)
                      (&DAT_006d5148 + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 0x14:
          local_5c = *(ushort *)
                      (&DAT_006d514a + *(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38);
          break;
        case 0x15:
          local_5c = (ushort)(byte)(&DAT_006d514c)
                                   [*(short *)(local_40 + (local_c & 0xffff) * 2 + 0x62) * 0x38];
        }
        if (-1 < (short)local_5c) {
          local_10 = &DAT_0061bf90;
          FUN__text__004d2790(&DAT_0061bf90,1,0x4a,(local_54 & 0xffff) * 0x2b + 0x367,
                              local_34[(local_44 & 0xffff) * 2 + 1] + 0x5c +
                              (local_c & 0xffff) * 0x26,0,(bVar1 - 8) * 0x10);
          FUN__text__004b7230((local_54 & 0xffff) * 0x2b + 0x377,
                              local_34[(local_44 & 0xffff) * 2 + 1] + 0x5d +
                              (local_c & 0xffff) * 0x26,0,0,2,0x4a,0x3f,(int)(short)local_5c,1);
          local_54 = CONCAT22(local_54._2_2_,(short)local_54 + 1);
        }
        local_58 = CONCAT22(local_58._2_2_,(short)local_58 + 1);
      }
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  if (DAT_007d7704 != 0) {
    local_10 = &DAT_0061bfa0;
    FUN__text__004d2790(&DAT_0061bfa0,1,0x4a,0x1d1,0x108,0,DAT_007d7704 * 0x18);
  }
  local_8 = 0x4b284a;
  FUN__text__0056ce80();
  return;
}

