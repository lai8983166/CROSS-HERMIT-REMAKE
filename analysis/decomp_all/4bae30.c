
void FUN__text__004bae30(void)

{
  ushort uVar1;
  int iVar2;
  ushort uVar3;
  undefined4 *puVar4;
  undefined4 local_74 [16];
  short local_34;
  short local_30;
  short local_2c;
  short local_28;
  uint local_24;
  uint local_20;
  ushort local_1c;
  undefined2 uStack_1a;
  ushort local_18;
  undefined2 uStack_16;
  ushort local_14;
  undefined2 uStack_12;
  undefined4 local_10;
  uint local_c;
  int local_8;
  
  puVar4 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  FUN__text__004d2700(&DAT_0061c330,1,0x56,0,0);
  FUN__text__004d2790(&DAT_0061c370,1,0x55,0x10c,0x57,0,*(short *)(local_8 + 0x34) * 0x1c);
  FUN__text__004d2790(&DAT_0061c380,1,0x55,0x15a,0x77,0,*(short *)(local_8 + 0x36) * 0x1c);
  FUN__text__004d2790(&DAT_0061c390,1,0x55,0x143,0x94,0,*(short *)(local_8 + 0x38) * 0x18);
  FUN__text__004bb520(0x1c7,0xc6,0,0,9,0x55,*(undefined4 *)(local_8 + 0x3c),0xd,1,3,7,0,
                      &DAT_0061c360,&DAT_0061c410);
  FUN__text__004bb520(0x1bc,0xe6,0,0,9,0x55,*(undefined4 *)(local_8 + 0x40),10,1,3,7,0,&DAT_0061c350
                      ,&DAT_0061c400);
  FUN__text__004bb520(0x1bc,0x102,0,0,9,0x55,*(undefined4 *)(local_8 + 0x44),10,1,3,7,0,
                      &DAT_0061c350,&DAT_0061c400);
  FUN__text__004bb520(400,0x132,0,0,2,0x55,(int)*(short *)(local_8 + 0x48),0xd,1,2,5,0,&DAT_0061c360
                      ,&DAT_0061c410);
  FUN__text__004bb520(0x173,0x154,0,0x14,4,0x55,(int)*(short *)(local_8 + 0x4a),10,1,2,5,0,
                      &DAT_0061c350,&DAT_0061c400);
  FUN__text__004bb520(400,0x154,0,0x14,8,0x55,(int)*(short *)(local_8 + 0x4c),10,1,2,1,0,
                      &DAT_0061c350,&DAT_0061c400);
  FUN__text__004bb520(400,0x170,0,0x28,4,0x55,(int)*(short *)(local_8 + 0x4e),10,1,2,5,0,
                      &DAT_0061c350,&DAT_0061c400);
  local_10 = (uint)local_10._2_2_ << 0x10;
  while ((local_10 & 0xffff) < 7) {
    local_c = local_c & 0xffff0000;
    while ((local_c & 0xffff) < 10) {
      if (0 < *(short *)(local_8 + 0x140 + (local_10 & 0xffff) * 0x14 + (local_c & 0xffff) * 2)) {
        uVar1 = *(short *)(local_8 + 0x140 + (local_10 & 0xffff) * 0x14 + (local_c & 0xffff) * 2) -
                1;
        _local_14 = CONCAT22(uStack_12,uVar1);
        _local_18 = CONCAT22(uStack_16,uVar1 % 0xc);
        _local_1c = CONCAT22(uStack_1a,uVar1 / 0xc);
        FUN__text__004d2790(&DAT_0061c3d0,1,0x55,(local_c & 0xffff) * 0x24 + 0xab,
                            (local_10 & 0xffff) * 0x24 + 0x1bd,(uVar1 % 0xc) * 0x24,
                            (uint)(uVar1 / 0xc) * 0x24);
      }
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
    local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
  }
  local_10 = local_10 & 0xffff0000;
  while ((local_10 & 0xffff) < 5) {
    local_c = local_c & 0xffff0000;
    while ((local_c & 0xffff) < 4) {
      if (*(short *)(local_8 + 0x50 + (local_10 & 0xffff) * 8 + (local_c & 0xffff) * 2) < 1) {
        FUN__text__004d2620((local_c & 0xffff) * 0x66 + 0x230,(local_10 & 0xffff) * 0x7e + 0x4a,0x61
                            ,0x76,0x35,0xa0010101,1);
      }
      else {
        uVar1 = (short)local_c * 0x66 + 0x22f;
        local_20 = CONCAT22(local_20._2_2_,uVar1);
        uVar3 = (short)local_10 * 0x7e + 0x4a;
        local_24 = CONCAT22(local_24._2_2_,uVar3);
        local_2c = *(short *)(local_8 + 0x50 + (local_10 & 0xffff) * 8 + (local_c & 0xffff) * 2) +
                   -1;
        local_28 = local_2c;
        FUN__text__004d2790(&DAT_0061c3b0,1,0x54,uVar1 + 0x11,uVar3 + 2,0,(int)local_2c << 4);
        local_30 = local_28 / 0xd;
        local_34 = local_28 % 0xd;
        FUN__text__004d2790(&DAT_0061c3c0,1,0x55,(local_20 & 0xffff) + 0x11,
                            (local_24 & 0xffff) + 0x12,(int)local_30 << 6,local_34 * 0x4e);
        FUN__text__004d2790(&DAT_0061c3e0,1,0x54,(local_20 & 0xffff) + 0x20,
                            (local_24 & 0xffff) + 0x14,0,0x10);
        FUN__text__004bb520((local_20 & 0xffff) + 0x20,(local_24 & 0xffff) + 0x14,0,0x10,3,0x54,
                            (int)*(short *)(local_8 + 0x78 + (local_10 & 0xffff) * 8 +
                                           (local_c & 0xffff) * 2),8,1,3,7,0,&DAT_0061c340,
                            &DAT_0061c3f0);
        FUN__text__004bb520((local_20 & 0xffff) + 0x27,(local_24 & 0xffff) + 0x14,0,0x10,5,0x54,
                            (int)*(short *)(local_8 + 0xa0 + (local_10 & 0xffff) * 8 +
                                           (local_c & 0xffff) * 2),8,1,3,3,0,&DAT_0061c340,
                            &DAT_0061c3f0);
        FUN__text__004bb520((local_20 & 0xffff) + 0x5f,(local_24 & 0xffff) + 0x4a,0,0x20,3,0x54,
                            (int)*(short *)(local_8 + 200 + (local_10 & 0xffff) * 8 +
                                           (local_c & 0xffff) * 2),8,1,3,7,0,&DAT_0061c340,
                            &DAT_0061c3f0);
        FUN__text__004bb520((local_20 & 0xffff) + 0x60,(local_24 & 0xffff) + 100,0,0,9,0x54,
                            *(undefined4 *)
                             (local_8 + 0xf0 + (local_10 & 0xffff) * 0x10 + (local_c & 0xffff) * 4),
                            8,1,3,7,0,&DAT_0061c340,&DAT_0061c3f0);
      }
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
    local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
  }
  FUN__text__004d2700(&DAT_0061c320,1,0x33,*(undefined2 *)(DAT_007a49fc + 0x196c),
                      *(undefined2 *)(DAT_007a49fc + 0x1970));
  local_8 = 0x4bb50f;
  FUN__text__0056ce80();
  return;
}

