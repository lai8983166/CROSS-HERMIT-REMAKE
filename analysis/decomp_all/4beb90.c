
void FUN__text__004beb90(undefined2 param_1,undefined2 param_2,short param_3,ushort param_4,
                        char param_5,undefined4 param_6,undefined1 param_7,short param_8)

{
  ushort uVar1;
  byte bVar2;
  short sVar3;
  short sVar4;
  int iVar5;
  int iVar6;
  undefined2 uVar7;
  undefined4 *puVar8;
  undefined4 local_6c [16];
  int local_2c;
  undefined2 local_28;
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
  
  iVar5 = 0x1a;
  puVar8 = local_6c;
  while( true ) {
    if (iVar5 == 0) break;
    iVar5 = iVar5 + -1;
    *puVar8 = 0xcccccccc;
    puVar8 = puVar8 + 1;
  }
  local_2c = (int)param_3;
  switch(local_2c) {
  case 0:
    local_28 = 1;
    bVar2 = FUN__text__004d1ba0(param_4,0,10);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x15);
    break;
  case 1:
    local_28 = 2;
    bVar2 = FUN__text__004d1ba0(param_4,0,10);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x16);
    break;
  case 2:
    local_28 = 3;
    bVar2 = FUN__text__004d1ba0(param_4,0,10);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x17);
    break;
  case 3:
    local_28 = 0;
    bVar2 = FUN__text__004d1ba0(param_4,0,0x1f);
    param_4 = (ushort)bVar2;
    local_c = CONCAT22(local_c._2_2_,0x14);
  }
  _local_20 = CONCAT22(uStack_1e,param_4 / 0x18);
  _local_24 = CONCAT22(uStack_22,param_4 % 0x18);
  local_18 = CONCAT22(local_18._2_2_,*(short *)(&DAT_0061c608 + (local_c & 0xffff) * 0x10));
  uVar1 = *(ushort *)(&DAT_0061c60a + (local_c & 0xffff) * 0x10);
  _local_1c = CONCAT22(uStack_1a,uVar1);
  sVar3 = *(short *)(&DAT_0061c604 + (local_c & 0xffff) * 0x10) +
          (param_4 / 0x18) * *(short *)(&DAT_0061c608 + (local_c & 0xffff) * 0x10);
  _local_10 = CONCAT22(uStack_e,sVar3);
  iVar5 = (uint)(param_4 % 0x18) * (uint)uVar1;
  sVar4 = *(short *)(&DAT_0061c606 + (local_c & 0xffff) * 0x10) + (short)iVar5;
  _local_14 = CONCAT22(uStack_12,sVar4);
  if (param_5 != '\0') {
    local_18 = CONCAT22(local_18._2_2_,0x74);
  }
  uVar7 = (undefined2)((uint)iVar5 >> 0x10);
  iVar6 = (local_c & 0xffff) * 0x10;
  FUN__text__004d29e0(CONCAT31((int3)((uint)iVar6 >> 8),(&DAT_0061c600)[(local_c & 0xffff) * 0x10]),
                      CONCAT22(uVar7,*(undefined2 *)(&DAT_0061c602 + iVar6)),3,(int)param_8,
                      CONCAT22(uVar7,param_1),param_2,sVar3,CONCAT22(uVar7,sVar4),local_18 & 0xffff,
                      uVar1,100,100,CONCAT31((int3)((uint)iVar5 >> 8),param_7),0x80,0x80,0x80);
  local_8 = 0x4beddb;
  FUN__text__0056ce80();
  return;
}

