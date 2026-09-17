
void __fastcall FUN__text__0049faa0(undefined4 param_1)

{
  ushort uVar1;
  int iVar2;
  ushort uVar3;
  uint uVar4;
  undefined4 *puVar5;
  undefined4 local_88 [16];
  ushort local_48;
  undefined2 uStack_46;
  ushort local_44;
  undefined2 uStack_42;
  undefined2 local_40;
  undefined2 uStack_3e;
  ushort local_3c;
  undefined2 uStack_3a;
  ushort local_38;
  undefined2 uStack_36;
  undefined2 local_34;
  undefined2 uStack_32;
  short local_30;
  short local_2c;
  uint local_28;
  undefined *local_24;
  short local_20 [12];
  undefined4 local_8;
  
  puVar5 = local_88;
  for (iVar2 = 0x21; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_8 = param_1;
  local_20[0] = 3;
  local_20[1] = 0x39;
  local_20[2] = 4;
  local_20[3] = 0x39;
  local_20[4] = 5;
  local_20[5] = 0x39;
  local_20[6] = 10;
  local_20[7] = 0x3a;
  local_20[8] = 0xb;
  local_20[9] = 0x3a;
  local_20[10] = 0xffff;
  local_20[0xb] = 0xffff;
  local_28 = local_28 & 0xffff0000;
  while( true ) {
    local_2c = local_20[(local_28 & 0xffff) * 2];
    local_30 = local_20[(local_28 & 0xffff) * 2 + 1];
    if (local_2c == -1) break;
    iVar2 = local_2c * 0x10;
    local_24 = &DAT_0061b050 + iVar2;
    FUN__text__004d2700(local_24,1,(int)local_30,
                        CONCAT22((short)((uint)local_24 >> 0x10),
                                 *(undefined2 *)(&DAT_0061b05c + iVar2)),
                        CONCAT22(local_2c >> 0xf,*(undefined2 *)(&DAT_0061b05e + iVar2)));
    local_28 = CONCAT22(local_28._2_2_,(short)local_28 + 1);
  }
  uVar4 = (DAT_007a528e + -1) % 0xc;
  _local_34 = CONCAT22(uStack_32,(short)uVar4);
  uVar1 = (ushort)((ulonglong)(uVar4 & 0xffff) / 6);
  _local_38 = CONCAT22(uStack_36,uVar1);
  uVar3 = (ushort)((ulonglong)(uVar4 & 0xffff) % 6);
  _local_3c = CONCAT22(uStack_3a,uVar3);
  local_24 = &DAT_0061b0b0;
  FUN__text__004d2790(&DAT_0061b0b0,1,0x39,CONCAT22(0x61,DAT_0061b0bc),CONCAT22(0x61,DAT_0061b0be),
                      (uint)uVar1 * (uint)DAT_0061b0b8,(uint)uVar3 * (uint)DAT_0061b0ba);
  uVar4 = (DAT_007a5290 + -1) % 9;
  _local_40 = CONCAT22(uStack_3e,(short)uVar4);
  uVar1 = (ushort)((ulonglong)(uVar4 & 0xffff) / 5);
  _local_44 = CONCAT22(uStack_42,uVar1);
  uVar3 = (ushort)((ulonglong)(uVar4 & 0xffff) % 5);
  _local_48 = CONCAT22(uStack_46,uVar3);
  local_24 = &DAT_0061b0c0;
  FUN__text__004d2790(&DAT_0061b0c0,1,0x39,CONCAT22(0x61,DAT_0061b0cc),CONCAT22(0x61,DAT_0061b0ce),
                      (uint)uVar1 * (uint)DAT_0061b0c8,(uint)uVar3 * (uint)DAT_0061b0ca);
  local_24 = &DAT_0061b070;
  FUN__text__004d2700(&DAT_0061b070,1,0x3d,0,0);
  FUN__text__004d2700(&DAT_0061b050,1,0x33,*(undefined2 *)(DAT_007a49fc + 0x196c),
                      *(undefined2 *)(DAT_007a49fc + 0x1970));
  FUN__text__004d69e0();
  local_8 = 0x49fd3e;
  FUN__text__0056ce80();
  return;
}

