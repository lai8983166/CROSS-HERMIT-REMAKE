
void FUN__text__004aaf60(short param_1,short param_2,char param_3,short param_4,undefined1 param_5,
                        undefined2 param_6)

{
  short sVar1;
  uint uVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  short sVar6;
  uint uVar7;
  uint uVar8;
  undefined4 *puVar9;
  undefined4 local_64 [16];
  char local_24;
  undefined2 local_20;
  undefined2 uStack_1e;
  short local_1c;
  undefined2 uStack_1a;
  undefined2 local_18;
  undefined2 uStack_16;
  short local_14;
  undefined2 uStack_12;
  undefined2 local_10;
  undefined2 uStack_e;
  uint local_c;
  undefined4 local_8;
  
  puVar9 = local_64;
  for (iVar3 = 0x18; uVar2 = local_c, iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar9 = 0xcccccccc;
    puVar9 = puVar9 + 1;
  }
  local_c = local_c & 0xffffff00;
  uVar4 = local_c;
  local_24 = param_3;
  local_c._1_3_ = SUB43(uVar2,1);
  if (param_3 == '\0') {
    local_c = CONCAT31(local_c._1_3_,3);
    uVar4 = local_c;
  }
  else if (param_3 == '\x01') {
    local_c = CONCAT31(local_c._1_3_,4);
    uVar4 = local_c;
  }
  local_c = uVar4;
  uVar4 = local_c & 0xff;
  _local_20 = CONCAT22(uStack_1e,*(undefined2 *)(&DAT_0061b20a + uVar4 * 0x10));
  uVar2 = local_c & 0xff;
  uVar7 = local_c & 0xff;
  uVar5 = local_c & 0xff;
  _local_18 = CONCAT22(uStack_16,*(undefined2 *)(&DAT_0061b210 + uVar5 * 0x10));
  sVar1 = *(short *)(&DAT_0061b212 + (local_c & 0xff) * 0x10);
  _local_1c = CONCAT22(uStack_1a,sVar1);
  uVar8 = local_c & 0xff;
  local_c = CONCAT31(local_c._1_3_,(&DAT_0061b208)[uVar8 * 0x10]);
  _local_10 = CONCAT22(uStack_e,*(undefined2 *)(&DAT_0061b20c + uVar2 * 0x10));
  sVar6 = *(short *)(&DAT_0061b20e + uVar7 * 0x10) + sVar1 * param_4;
  _local_14 = CONCAT22(uStack_12,sVar6);
  FUN__text__004d3050(CONCAT31((int3)(char)((ushort)param_1 >> 8),(&DAT_0061b208)[uVar8 * 0x10]),
                      param_6,*(undefined2 *)(&DAT_0061b20a + uVar4 * 0x10),(int)param_1,
                      (int)param_2,*(undefined2 *)(&DAT_0061b20c + uVar2 * 0x10),sVar6,
                      *(undefined2 *)(&DAT_0061b210 + uVar5 * 0x10),sVar1,param_5,0x80,0x80,0x80);
  local_8 = 0x4ab0c7;
  FUN__text__0056ce80();
  return;
}

