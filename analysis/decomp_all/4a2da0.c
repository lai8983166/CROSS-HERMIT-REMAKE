
/* WARNING: Removing unreachable block (ram,0x004a2eb1) */
/* WARNING: Removing unreachable block (ram,0x004a30b0) */
/* WARNING: Removing unreachable block (ram,0x004a2f12) */

void FUN__text__004a2da0(void)

{
  ushort uVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_8c [16];
  short local_4c;
  short local_48;
  short local_44;
  short local_40;
  short local_3c;
  undefined1 local_38;
  uint local_34;
  undefined2 local_30;
  undefined2 uStack_2e;
  uint local_2c;
  uint local_28;
  uint local_24;
  short local_20;
  short local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  iVar2 = 0x22;
  puVar4 = local_8c;
  while( true ) {
    if (iVar2 == 0) break;
    iVar2 = iVar2 + -1;
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_1c = 0;
  local_20 = FUN__text__004a8bc0();
  if ((&DAT_007aaa15)[local_20 * 0x1c] != '\0') {
    local_1c = 1;
  }
  uVar1 = (ushort)DAT_007d598a;
  local_24 = CONCAT22(local_24._2_2_,uVar1);
  local_28 = CONCAT22(local_28._2_2_,(&DAT_007d6a14)[uVar1]);
  if ((&DAT_007d6a14)[uVar1] != 0) {
    _local_30 = CONCAT22(uStack_2e,*(undefined2 *)(&DAT_007d6a1a + (uint)uVar1 * 2));
    local_38 = 0x80;
    local_2c = local_2c & 0xffff0000;
    while ((local_2c & 0xffff) < 10) {
      local_38 = 0x80;
      local_34 = CONCAT22(local_34._2_2_,(ushort)local_2c + (short)_local_30 * 2);
      if ((local_28 & 0xffff) <= (local_2c & 0xffff)) break;
      local_3c = ((ushort)local_2c & 1) * 0x79 + 0x298;
      local_40 = (short)((local_2c & 0xffff) / 2) * 0x17 + 0x1be;
      if (local_1c != 0) {
        FUN__text__004d5ec0(local_18,(local_2c & 1) * 0x79 + 0x298,
                            ((local_2c & 0xffff) / 2) * 0x17 + 0x1be,0x70,0x16);
        local_38 = 0x80;
        if (((local_c & 0xffff) != 0) && (local_38 = 0xff, (local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          local_44 = FUN__text__004a8bc0();
          *(undefined2 *)(&DAT_007aaa18 + local_44 * 0x1c) = (undefined2)local_24;
          *(undefined2 *)(&DAT_007aaa1a + local_44 * 0x1c) =
               *(undefined2 *)(&DAT_007d630c + (local_34 & 0xffff) * 6 + (local_24 & 0xffff) * 600);
          *(undefined2 *)(&DAT_007aaa1c + local_44 * 0x1c) =
               *(undefined2 *)(&DAT_007d630e + (local_34 & 0xffff) * 6 + (local_24 & 0xffff) * 600);
          *(undefined2 *)(&DAT_007aaa1e + local_44 * 0x1c) =
               *(undefined2 *)(&DAT_007d6310 + (local_34 & 0xffff) * 6 + (local_24 & 0xffff) * 600);
        }
      }
      local_48 = FUN__text__004a8bc0();
      if (((int)*(short *)(&DAT_007aaa18 + local_48 * 0x1c) == (local_24 & 0xffff)) &&
         ((int)*(short *)(&DAT_007aaa1a + local_48 * 0x1c) ==
          (uint)*(ushort *)(&DAT_007d630c + (local_34 & 0xffff) * 6 + (local_24 & 0xffff) * 600))) {
        local_38 = 0xff;
        FUN__text__004d2700(&DAT_0061b448,3,0x71,(local_2c & 1) * 0x79 + 0x28b,
                            ((local_2c & 0xffff) / 2) * 0x17 + 0x1bb);
      }
      iVar2 = (local_24 & 0xffff) * 600;
      iVar3 = (local_34 & 0xffff) * 6;
      FUN__text__004aa6c0(local_3c,CONCAT22((short)((uint)iVar3 >> 0x10),local_40),
                          CONCAT22((short)((uint)iVar2 >> 0x10),(undefined2)local_24),
                          *(undefined2 *)(&DAT_007d630c + iVar3 + iVar2),local_38,0x73);
      local_2c = CONCAT22(local_2c._2_2_,(short)local_2c + 1);
    }
    local_4c = FUN__text__004a8bc0();
    *(undefined2 *)(local_8 + 0x1290) = *(undefined2 *)(&DAT_007aaa1c + local_4c * 0x1c);
    if ((*(short *)(local_8 + 0x1290) != 0) && (*(short *)(local_8 + 0x1290) != -1)) {
      if (*(short *)(local_8 + 0x1292) != *(short *)(local_8 + 0x1290)) {
        FUN__text__004d64d0(*(undefined2 *)(local_8 + 0x1290),10);
        if (*(short *)(local_8 + 0x1290) < 1) {
          DAT_007d598a = '\0';
        }
        else {
          DAT_007d598a = (char)*(undefined2 *)(&DAT_0074bed6 + *(short *)(local_8 + 0x1290) * 0x60)
                         + -1;
        }
        *(undefined2 *)(local_8 + 0x1292) = *(undefined2 *)(local_8 + 0x1290);
      }
      FUN__text__004d62f0(0x244,0x23e,0x79);
    }
  }
  local_8 = 0x4a3235;
  FUN__text__0056ce80();
  return;
}

