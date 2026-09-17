
void FUN__text__004aadb0(short param_1,short param_2,char param_3,uint param_4,undefined4 param_5,
                        undefined1 param_6,undefined2 param_7)

{
  short sVar1;
  short sVar2;
  short sVar3;
  short sVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  undefined4 *puVar8;
  undefined4 local_68 [16];
  char local_28;
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
  
  puVar8 = local_68;
  for (iVar5 = 0x19; uVar6 = local_c, iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar8 = 0xcccccccc;
    puVar8 = puVar8 + 1;
  }
  local_c = local_c & 0xffffff00;
  uVar7 = local_c;
  local_24 = 1;
  local_28 = param_3;
  local_c._1_3_ = SUB43(uVar6,1);
  if (param_3 == '\0') {
    local_24 = 0xe;
    local_c = CONCAT31(local_c._1_3_,1);
    uVar7 = local_c;
  }
  else if (param_3 == '\x01') {
    local_24 = 7;
    local_c = CONCAT31(local_c._1_3_,2);
    uVar7 = local_c;
  }
  local_c = uVar7;
  uVar6 = local_c & 0xff;
  _local_20 = CONCAT22(uStack_1e,*(undefined2 *)(&DAT_0061b20a + uVar6 * 0x10));
  sVar1 = *(short *)(&DAT_0061b210 + (local_c & 0xff) * 0x10);
  _local_18 = CONCAT22(uStack_16,sVar1);
  sVar2 = *(short *)(&DAT_0061b212 + (local_c & 0xff) * 0x10);
  _local_1c = CONCAT22(uStack_1a,sVar2);
  sVar3 = *(short *)(&DAT_0061b20c + (local_c & 0xff) * 0x10) +
          sVar1 * (short)((ulonglong)(param_4 & 0xffff) / (ulonglong)(longlong)(int)local_24);
  _local_10 = CONCAT22(uStack_e,sVar3);
  sVar4 = *(short *)(&DAT_0061b20e + (local_c & 0xff) * 0x10) +
          sVar2 * (short)((ulonglong)(param_4 & 0xffff) % (ulonglong)(longlong)(int)local_24);
  _local_14 = CONCAT22(uStack_12,sVar4);
  uVar7 = local_c & 0xff;
  local_c = CONCAT31(local_c._1_3_,(&DAT_0061b208)[uVar7 * 0x10]);
  FUN__text__004d3050(CONCAT31((int3)(char)((ushort)param_1 >> 8),(&DAT_0061b208)[uVar7 * 0x10]),
                      param_7,*(undefined2 *)(&DAT_0061b20a + uVar6 * 0x10),(int)param_1,
                      (int)param_2,sVar3,sVar4,sVar1,sVar2,param_6,0x80,0x80,0x80);
  local_8 = 0x4aaf53;
  FUN__text__0056ce80();
  return;
}

