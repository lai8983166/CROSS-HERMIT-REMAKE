
/* WARNING: Removing unreachable block (ram,0x004c9808) */

void __thiscall
FUN__text__004c97a0(int param_1,short param_2,short param_3,undefined2 param_4,ushort param_5,
                   uint param_6,undefined2 param_7)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  short sVar5;
  int iVar6;
  short sVar7;
  undefined4 *puVar8;
  undefined4 local_88 [16];
  uint local_48;
  undefined2 local_44;
  undefined2 uStack_42;
  short local_40;
  short local_3c;
  short local_38;
  short local_34;
  undefined2 local_30;
  undefined2 uStack_2e;
  undefined2 local_2c;
  undefined2 uStack_2a;
  undefined2 local_28;
  undefined2 uStack_26;
  int local_24;
  undefined2 local_20;
  undefined2 uStack_1e;
  short local_1c;
  short local_18;
  short local_14;
  undefined2 uStack_12;
  short local_10;
  undefined2 uStack_e;
  int local_c;
  int local_8;
  
  puVar8 = local_88;
  for (iVar6 = 0x21; iVar6 != 0; iVar6 = iVar6 + -1) {
    *puVar8 = 0xcccccccc;
    puVar8 = puVar8 + 1;
  }
  local_48 = (uint)*(ushort *)(param_1 + 0x30);
  local_8 = param_1;
  if (local_48 == 0) {
    local_24 = *(int *)(param_1 + 0x44 + (param_6 & 0xff) * 4);
    uVar1 = *(undefined2 *)(local_24 + 0xc + (uint)param_5 * 6);
    _local_28 = CONCAT22(uStack_26,uVar1);
    uVar2 = *(undefined2 *)(local_24 + 0xe + (uint)param_5 * 6);
    _local_2c = CONCAT22(uStack_2a,uVar2);
    uVar3 = *(undefined2 *)(local_24 + 0x10 + (uint)param_5 * 6);
    _local_30 = CONCAT22(uStack_2e,uVar3);
    local_34 = param_2 + *(short *)(local_24 + 4);
    local_38 = param_3 + *(short *)(local_24 + 6);
    local_3c = *(short *)(local_24 + 8);
    local_40 = *(short *)(local_24 + 10);
    uVar4 = *(undefined2 *)(param_1 + 0x40 + (param_6 & 0xff) * 2);
    _local_44 = CONCAT22(uStack_42,uVar4);
    FUN__text__004cbdb0((int)local_34,(int)local_38,param_4,0xffffffff,param_7,uVar2,uVar3,
                        (int)local_3c,(int)local_40,uVar4,uVar1);
  }
  else if (local_48 == 1) {
    local_c = *(int *)(param_1 + 0x44 + (param_6 & 0xff) * 4);
    sVar7 = (param_5 & 3) << 7;
    _local_10 = CONCAT22(uStack_e,sVar7);
    sVar5 = (short)(((int)(uint)param_5 >> 2) << 7) + 0x300;
    _local_14 = CONCAT22(uStack_12,sVar5);
    local_18 = param_2 + *(short *)(local_c + 4);
    local_1c = param_3 + *(short *)(local_c + 6);
    uVar1 = *(undefined2 *)(param_1 + 0x40 + (param_6 & 0xff) * 2);
    _local_20 = CONCAT22(uStack_1e,uVar1);
    FUN__text__004cbdb0((int)local_18,(int)local_1c,param_4,0xffffffff,param_7,sVar7,sVar5,0x80,0x80
                        ,uVar1,0);
  }
  local_8 = 0x4c99d9;
  FUN__text__0056ce80();
  return;
}

