
void FUN__text__004aa7e0(short param_1,short param_2,short param_3,ushort param_4,char param_5,
                        char param_6,undefined1 param_7,short param_8)

{
  ushort uVar1;
  byte bVar2;
  short sVar3;
  short sVar4;
  int iVar5;
  undefined2 extraout_var;
  int iVar6;
  undefined2 uVar7;
  undefined2 extraout_var_00;
  undefined4 *puVar8;
  undefined4 local_84 [16];
  char local_44;
  int local_40;
  undefined *local_3c;
  ushort local_38;
  undefined2 uStack_36;
  uint local_34;
  undefined4 local_30;
  undefined2 local_2c;
  uint local_28;
  ushort local_24;
  undefined2 uStack_22;
  ushort local_20;
  undefined2 uStack_1e;
  ushort local_1c;
  undefined2 uStack_1a;
  uint local_18;
  short local_14;
  undefined2 uStack_12;
  short local_10;
  undefined2 uStack_e;
  uint local_c;
  undefined4 local_8;
  
  iVar5 = 0x20;
  puVar8 = local_84;
  while( true ) {
    if (iVar5 == 0) break;
    iVar5 = iVar5 + -1;
    *puVar8 = 0xcccccccc;
    puVar8 = puVar8 + 1;
  }
  local_40 = (int)param_3;
  switch(local_40) {
  case 0:
    local_30 = CONCAT22(local_30._2_2_,1);
    bVar2 = FUN__text__004d1ba0(param_4,0,10);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x28);
    break;
  case 1:
    local_30 = CONCAT22(local_30._2_2_,2);
    bVar2 = FUN__text__004d1ba0(param_4,0,10);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x29);
    break;
  case 2:
    local_30 = CONCAT22(local_30._2_2_,3);
    bVar2 = FUN__text__004d1ba0(param_4,0,10);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x2a);
    break;
  case 3:
    local_30 = (uint)local_30._2_2_ << 0x10;
    bVar2 = FUN__text__004d1ba0(param_4,0,0x1f);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x27);
    param_6 = '\x01';
  }
  if (param_5 == '\0') {
    local_3c = &DAT_0061b468;
    uVar7 = (undefined2)(param_1 + 0x83);
    local_28 = CONCAT22(local_28._2_2_,uVar7);
    local_2c = (undefined2)(param_2 + 5);
    local_44 = param_6;
    if (param_6 == -1) {
      local_34 = CONCAT22(local_34._2_2_,10);
      _local_38 = CONCAT22(uStack_36,10);
      iVar5 = (uint)DAT_0061b46c + (uint)DAT_0061b470 * 10;
      FUN__text__004d28c0(&DAT_0061b468,3,(int)param_8,CONCAT22(0x61,uVar7),
                          CONCAT22((short)((uint)iVar5 >> 0x10),local_2c),iVar5,
                          (uint)DAT_0061b46e + (uint)DAT_0061b472 * (local_30 & 0xffff),
                          CONCAT22(0x61,DAT_0061b470),DAT_0061b472,
                          CONCAT31((int3)((uint)(param_1 + 0x83) >> 8),param_7));
      iVar5 = (uint)*(ushort *)(local_3c + 4) + (uint)*(ushort *)(local_3c + 8) * 10;
      FUN__text__004d28c0(local_3c,3,(int)param_8,(local_28 & 0xffff) + 10,
                          CONCAT22((short)((uint)iVar5 >> 0x10),local_2c),iVar5,
                          (uint)*(ushort *)(local_3c + 6) +
                          (uint)*(ushort *)(local_3c + 10) * (local_30 & 0xffff),
                          *(undefined2 *)(local_3c + 8),
                          CONCAT22(extraout_var_00,*(undefined2 *)(local_3c + 10)),param_7);
    }
    else if (param_6 == '\x01') {
      FUN__text__004d28c0(&DAT_0061b468,3,(int)param_8,param_1 + 0x74,
                          CONCAT22((short)((uint)(param_2 + 5) >> 0x10),param_2),0x11c,
                          (local_30 & 0xffff) * 0x16 + 0x1a2,0x2c,0x16,param_7);
    }
    else {
      local_34 = CONCAT22(local_34._2_2_,(short)param_6 % 10);
      _local_38 = CONCAT22(uStack_36,(short)param_6 / 10);
      iVar5 = (uint)DAT_0061b470 * (uint)(ushort)((short)param_6 / 10);
      iVar6 = (uint)DAT_0061b46c + iVar5;
      FUN__text__004d28c0(&DAT_0061b468,3,(int)param_8,CONCAT22((short)((uint)iVar6 >> 0x10),uVar7),
                          CONCAT22((short)((uint)iVar5 >> 0x10),local_2c),iVar6,
                          (uint)DAT_0061b46e + (uint)DAT_0061b472 * (local_30 & 0xffff),
                          CONCAT22(0x61,DAT_0061b470),DAT_0061b472,
                          CONCAT31((int3)((uint)((int)param_6 % 10) >> 8),param_7));
      iVar5 = (uint)*(ushort *)(local_3c + 8) * (local_34 & 0xffff);
      FUN__text__004d28c0(local_3c,3,(int)param_8,(local_28 & 0xffff) + 10,
                          CONCAT22((short)((uint)iVar5 >> 0x10),local_2c),
                          (uint)*(ushort *)(local_3c + 4) + iVar5,
                          (uint)*(ushort *)(local_3c + 6) +
                          (uint)*(ushort *)(local_3c + 10) * (local_30 & 0xffff),
                          *(undefined2 *)(local_3c + 8),
                          CONCAT22(extraout_var,*(undefined2 *)(local_3c + 10)),param_7);
    }
  }
  _local_20 = CONCAT22(uStack_1e,param_4 / 0x17);
  _local_24 = CONCAT22(uStack_22,param_4 % 0x17);
  local_18 = CONCAT22(local_18._2_2_,*(short *)(&DAT_0061b210 + (local_c & 0xffff) * 0x10));
  uVar1 = *(ushort *)(&DAT_0061b212 + (local_c & 0xffff) * 0x10);
  _local_1c = CONCAT22(uStack_1a,uVar1);
  sVar3 = *(short *)(&DAT_0061b20c + (local_c & 0xffff) * 0x10) +
          (param_4 / 0x17) * *(short *)(&DAT_0061b210 + (local_c & 0xffff) * 0x10);
  _local_10 = CONCAT22(uStack_e,sVar3);
  iVar5 = (uint)(param_4 % 0x17) * (uint)uVar1;
  sVar4 = *(short *)(&DAT_0061b20e + (local_c & 0xffff) * 0x10) + (short)iVar5;
  _local_14 = CONCAT22(uStack_12,sVar4);
  if (param_5 != '\0') {
    local_18 = CONCAT22(local_18._2_2_,0x74);
  }
  uVar7 = (undefined2)((uint)iVar5 >> 0x10);
  iVar6 = (local_c & 0xffff) * 0x10;
  FUN__text__004d29e0(CONCAT31((int3)((uint)iVar6 >> 8),(&DAT_0061b208)[(local_c & 0xffff) * 0x10]),
                      CONCAT22(uVar7,*(undefined2 *)(&DAT_0061b20a + iVar6)),3,(int)param_8,
                      CONCAT22(uVar7,param_1),param_2,sVar3,CONCAT22(uVar7,sVar4),local_18 & 0xffff,
                      uVar1,100,100,CONCAT31((int3)((uint)iVar5 >> 8),param_7),0x80,0x80,0x80);
  local_8 = 0x4aaccd;
  FUN__text__0056ce80();
  return;
}

