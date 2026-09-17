
void FUN__text__004b84f0(undefined2 param_1,undefined2 param_2,uint param_3,char param_4,
                        undefined2 param_5)

{
  uint uVar1;
  ushort uVar2;
  int iVar3;
  ushort uVar4;
  undefined4 *puVar5;
  undefined4 local_5c [16];
  char local_1c;
  uint local_18;
  ushort local_14;
  undefined2 uStack_12;
  ushort local_10;
  undefined2 uStack_e;
  undefined *local_c;
  undefined4 local_8;
  
  puVar5 = local_5c;
  for (iVar3 = 0x16; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_c = &DAT_0061bef0;
  uVar4 = (ushort)((ulonglong)(param_3 & 0xffff) % 5);
  _local_10 = CONCAT22(uStack_e,uVar4);
  uVar2 = (ushort)((ulonglong)(param_3 & 0xffff) / 5);
  _local_14 = CONCAT22(uStack_12,uVar2);
  uVar1 = local_18 >> 0x10;
  local_18 = local_18 & 0xffff0000;
  local_1c = param_4;
  if (param_4 == '\x02') {
    local_18 = CONCAT22((short)uVar1,DAT_0061bef8);
  }
  iVar3 = (uint)uVar4 * (uint)DAT_0061bef8 * 2 + (local_18 & 0xffff);
  FUN__text__004d2790(&DAT_0061bef0,1,param_5,CONCAT22((short)((uint)iVar3 >> 0x10),param_1),
                      CONCAT22((short)((uint)DAT_0061bef8 * 2 >> 0x10),param_2),iVar3,
                      (uint)uVar2 * (uint)DAT_0061befa);
  local_8 = 0x4b85c3;
  FUN__text__0056ce80();
  return;
}

