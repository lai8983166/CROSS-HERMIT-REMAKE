
void __thiscall FUN__text__004cc9f0(int param_1,int param_2,int param_3)

{
  undefined2 uVar1;
  undefined2 uVar2;
  byte bVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_70 [16];
  byte local_30;
  undefined3 uStack_2f;
  int local_2c;
  short *local_28;
  byte local_24;
  undefined3 uStack_23;
  int local_20;
  short *local_1c;
  undefined2 local_18;
  undefined2 uStack_16;
  undefined2 local_14;
  undefined2 uStack_12;
  uint local_10;
  uint local_c;
  int local_8;
  
  iVar4 = 0x1b;
  puVar5 = local_70;
  while( true ) {
    if (iVar4 == 0) break;
    iVar4 = iVar4 + -1;
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_1c = (short *)(&DAT_00624520 + param_2 * 0x26);
  local_20 = param_1 + 0x6f60 + *local_1c * 0xe0;
  local_8 = param_1;
  bVar3 = FUN__text__004ca9b0();
  _local_24 = CONCAT31(uStack_23,bVar3);
  local_c = CONCAT22(local_c._2_2_,*(undefined2 *)(local_20 + 0x34 + (uint)bVar3 * 2));
  local_10 = CONCAT22(local_10._2_2_,*(undefined2 *)(local_20 + 0x38 + (uint)bVar3 * 2));
  local_28 = (short *)(&DAT_00624520 + param_3 * 0x26);
  local_2c = local_8 + 0x6f60 + *local_28 * 0xe0;
  bVar3 = FUN__text__004ca9b0();
  _local_30 = CONCAT31(uStack_2f,bVar3);
  uVar1 = *(undefined2 *)(local_2c + 0x34 + (uint)bVar3 * 2);
  _local_14 = CONCAT22(uStack_12,uVar1);
  uVar2 = *(undefined2 *)(local_2c + 0x38 + (uint)bVar3 * 2);
  _local_18 = CONCAT22(uStack_16,uVar2);
  FUN__text__004cc0f0(param_2,uVar1,uVar2);
  FUN__text__004cc0f0(param_3,local_c & 0xffff,local_10 & 0xffff);
  local_8 = 0x4ccb1c;
  FUN__text__0056ce80();
  return;
}

