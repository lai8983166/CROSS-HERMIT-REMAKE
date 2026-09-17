
void FUN__text__004b8140(short param_1,short param_2,short param_3,short param_4,undefined4 param_5,
                        undefined1 param_6,undefined2 param_7)

{
  short sVar1;
  short sVar2;
  uint uVar3;
  short sVar4;
  short sVar5;
  int iVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  undefined4 *puVar10;
  undefined4 local_68 [16];
  int local_28;
  short local_24;
  undefined2 local_20;
  undefined2 uStack_1e;
  short local_1c;
  undefined2 uStack_1a;
  short local_18;
  undefined2 uStack_16;
  short local_14;
  undefined2 uStack_12;
  short local_10;
  undefined2 uStack_e;
  uint local_c;
  undefined4 local_8;
  
  puVar10 = local_68;
  for (iVar6 = 0x19; uVar3 = local_c, iVar6 != 0; iVar6 = iVar6 + -1) {
    *puVar10 = 0xcccccccc;
    puVar10 = puVar10 + 1;
  }
  local_c = local_c & 0xffffff00;
  uVar7 = local_c;
  local_24 = 1;
  local_28 = (int)param_3;
  local_c._1_3_ = SUB43(uVar3,1);
  if (local_28 == 0) {
    local_24 = 0xe;
    local_c = CONCAT31(local_c._1_3_,10);
    uVar7 = local_c;
  }
  else if (local_28 == 1) {
    local_24 = 7;
    local_c = CONCAT31(local_c._1_3_,0xb);
    uVar7 = local_c;
  }
  local_c = uVar7;
  uVar7 = local_c & 0xff;
  _local_20 = CONCAT22(uStack_1e,*(undefined2 *)(&DAT_0061bae2 + uVar7 * 0x10));
  uVar3 = local_c & 0xff;
  uVar8 = local_c & 0xff;
  sVar1 = *(short *)(&DAT_0061bae8 + (local_c & 0xff) * 0x10);
  _local_18 = CONCAT22(uStack_16,sVar1);
  sVar2 = *(short *)(&DAT_0061baea + (local_c & 0xff) * 0x10);
  _local_1c = CONCAT22(uStack_1a,sVar2);
  uVar9 = local_c & 0xff;
  local_c = CONCAT31(local_c._1_3_,(&DAT_0061bae0)[uVar9 * 0x10]);
  sVar4 = *(short *)(&DAT_0061bae4 + uVar3 * 0x10) + sVar1 * (param_4 / local_24);
  _local_10 = CONCAT22(uStack_e,sVar4);
  sVar5 = *(short *)(&DAT_0061bae6 + uVar8 * 0x10) + sVar2 * (param_4 % local_24);
  _local_14 = CONCAT22(uStack_12,sVar5);
  FUN__text__004d3050(CONCAT31((int3)(char)((ushort)param_1 >> 8),(&DAT_0061bae0)[uVar9 * 0x10]),
                      param_7,*(undefined2 *)(&DAT_0061bae2 + uVar7 * 0x10),(int)param_1,
                      (int)param_2,sVar4,sVar5,sVar1,sVar2,param_6,0x80,0x80,0x80);
  local_8 = 0x4b82db;
  FUN__text__0056ce80();
  return;
}

