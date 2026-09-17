
void FUN__text__004aa6c0(undefined2 param_1,undefined2 param_2,short param_3,undefined2 param_4,
                        undefined1 param_5,short param_6)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  ushort uVar4;
  undefined4 *puVar5;
  undefined4 local_6c [16];
  int local_2c;
  undefined2 local_28;
  ushort local_24;
  undefined2 uStack_22;
  ushort local_20;
  undefined2 uStack_1e;
  undefined2 local_1c;
  undefined2 local_18;
  short local_14;
  short local_10;
  undefined2 local_c;
  undefined4 local_8;
  
  puVar5 = local_6c;
  for (iVar3 = 0x1a; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  bVar1 = FUN__text__004d1ba0(param_4,0,0x50);
  local_28 = 1;
  local_2c = (int)param_3;
  if (local_2c == 1) {
    local_c = 6;
  }
  else if (local_2c == 2) {
    local_c = 7;
  }
  else {
    local_c = 5;
  }
  uVar2 = bVar1 / 0x17;
  _local_20 = CONCAT22(uStack_1e,uVar2);
  uVar4 = (ushort)bVar1 % 0x17;
  _local_24 = CONCAT22(uStack_22,uVar4);
  local_10 = uVar2 * 0x74;
  local_14 = uVar4 * 0x16;
  local_18 = 0x74;
  local_1c = 0x16;
  FUN__text__004d29e0(0xc,local_c,3,(int)param_6,param_1,param_2,local_10,local_14,0x74,0x16,100,100
                      ,param_5,0x80,0x80,0x80);
  local_8 = 0x4aa7d9;
  FUN__text__0056ce80();
  return;
}

