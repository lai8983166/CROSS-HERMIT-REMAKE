
/* WARNING: Removing unreachable block (ram,0x004a21fd) */
/* WARNING: Removing unreachable block (ram,0x004a2130) */
/* WARNING: Removing unreachable block (ram,0x004a2303) */
/* WARNING: Removing unreachable block (ram,0x004a2194) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004a1ff0(void)

{
  ushort uVar1;
  int iVar2;
  uint uVar3;
  undefined2 uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_84 [16];
  short local_44;
  short local_40;
  short local_3c;
  undefined1 local_38;
  uint local_34;
  uint local_30;
  undefined2 local_2c;
  undefined2 uStack_2a;
  uint local_28;
  undefined4 local_24;
  short local_20;
  short local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  iVar2 = 0x20;
  puVar6 = local_84;
  while( true ) {
    if (iVar2 == 0) break;
    iVar2 = iVar2 + -1;
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_1c = 0;
  local_20 = FUN__text__004a8bc0();
  uVar3 = (uint)(char)(&DAT_007aaa15)[local_20 * 0x1c];
  if (uVar3 == 0) {
    local_1c = 1;
  }
  if (DAT_007a55fa == 0) {
    uVar3 = (uint)DAT_007d5984;
    if (uVar3 == 0) {
      local_24 = CONCAT22(local_24._2_2_,2);
    }
    else {
      local_24 = CONCAT22(local_24._2_2_,1);
    }
  }
  else {
    local_24 = (uint)local_24._2_2_ << 0x10;
  }
  DAT_007aab08 = (ushort)local_24;
  uVar4 = (undefined2)(uVar3 >> 0x10);
  local_28 = CONCAT22(local_28._2_2_,*(short *)(&DAT_007d62fa + (local_24 & 0xffff) * 2));
  if (*(short *)(&DAT_007d62fa + (local_24 & 0xffff) * 2) != 0) {
    _local_2c = CONCAT22(uStack_2a,*(undefined2 *)(&DAT_007d6300 + (local_24 & 0xffff) * 2));
    local_30 = local_30 & 0xffff0000;
    while ((local_30 & 0xffff) < 8) {
      uVar1 = (ushort)local_30 + (short)_local_2c * 2;
      local_34 = CONCAT22(local_34._2_2_,uVar1);
      if ((local_28 & 0xffff) <= (uint)uVar1) break;
      local_3c = ((ushort)local_30 & 1) * 0xa9 + 0x237;
      local_40 = (short)((local_30 & 0xffff) / 2) * 0x17 + 0x47;
      if (local_1c != 0) {
        FUN__text__004d5ec0(local_18,(local_30 & 1) * 0xa9 + 0x238,
                            ((local_30 & 0xffff) / 2) * 0x17 + 0x48,0xa2,0x14);
        local_38 = 0x80;
        if (((local_c & 0xffff) != 0) && (local_38 = 0xff, (local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          DAT_007aab0a = 1;
          _DAT_007aab0c = (ushort)local_30 & 1;
          _DAT_007aab0e = (undefined2)((local_30 & 0xffff) / 2);
          DAT_007aab10 = *(undefined2 *)
                          (&DAT_007d599a + (local_34 & 0xffff) * 10 + (local_24 & 0xffff) * 800);
          DAT_007aab12 = *(undefined2 *)
                          (&DAT_007d599c + (local_34 & 0xffff) * 10 + (local_24 & 0xffff) * 800);
          DAT_007aab16 = *(short *)(&DAT_007d599e +
                                   (local_34 & 0xffff) * 10 + (local_24 & 0xffff) * 800);
          DAT_007aab18 = (ushort)local_24;
          DAT_007aab14 = (ushort)local_34;
        }
        if (((uint)DAT_007aab18 == (local_24 & 0xffff)) &&
           ((uint)DAT_007aab14 == (local_34 & 0xffff))) {
          local_38 = 0xff;
          FUN__text__004d2700(&DAT_0061b438,3,0x71,(local_30 & 1) * 0xa9 + 0x229,
                              ((local_30 & 0xffff) / 2) * 0x17 + 0x44);
        }
      }
      iVar5 = (local_24 & 0xffff) * 800;
      iVar2 = (local_34 & 0xffff) * 10;
      FUN__text__004aa7e0(CONCAT22((short)((uint)iVar2 >> 0x10),local_3c),
                          CONCAT22((short)((uint)iVar5 >> 0x10),local_40),
                          *(undefined2 *)(&DAT_007d599a + iVar2 + iVar5),
                          *(undefined2 *)
                           (&DAT_007d599c + (local_34 & 0xffff) * 10 + (local_24 & 0xffff) * 800),0,
                          (&DAT_007d59a0)[(local_34 & 0xffff) * 10 + (local_24 & 0xffff) * 800],
                          local_38,0x75);
      local_30 = CONCAT22(local_30._2_2_,(short)local_30 + 1);
    }
    uVar4 = 0;
  }
  if (DAT_007aab0a != 0) {
    FUN__text__004aa7e0(0x60,0x2f,DAT_007aab10,CONCAT22(uVar4,DAT_007aab12),1,0,0xff,0x75);
    local_44 = DAT_007d5982 + -3 + DAT_007aab16 * 4;
    if (*(short *)(local_8 + 0x128e) != local_44) {
      FUN__text__004d64d0(local_44,0xb);
      *(short *)(local_8 + 0x128e) = local_44;
    }
    FUN__text__004d62f0(0x244,0xd8,0x79);
  }
  local_8 = 0x4a2496;
  FUN__text__0056ce80();
  return;
}

