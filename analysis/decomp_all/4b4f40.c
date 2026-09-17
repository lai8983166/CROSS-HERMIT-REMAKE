
void FUN__text__004b4f40(undefined2 param_1,undefined2 param_2,short param_3,short param_4,
                        undefined2 param_5)

{
  int iVar1;
  ushort uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  ushort local_20;
  undefined2 uStack_1e;
  ushort local_1c;
  undefined2 uStack_1a;
  ushort local_18;
  undefined2 uStack_16;
  short local_14;
  short local_10;
  undefined2 local_c;
  undefined4 local_8;
  
  puVar4 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = 0;
  local_10 = param_3;
  local_14 = param_4;
  uVar2 = param_3 * 7 + param_4;
  _local_18 = CONCAT22(uStack_16,uVar2);
  _local_1c = CONCAT22(uStack_1a,uVar2 / 0x15);
  _local_20 = CONCAT22(uStack_1e,uVar2 % 0x15);
  iVar3 = (uint)DAT_0061bc08 * (uint)(uVar2 / 0x15);
  iVar1 = (uint)DAT_0061bc04 + iVar3;
  FUN__text__004d2830(&DAT_0061bc00,1,param_5,CONCAT22((short)((uint)iVar3 >> 0x10),param_1),
                      CONCAT22((short)((uint)iVar1 >> 0x10),param_2),iVar1,
                      (uint)DAT_0061bc06 + (uint)DAT_0061bc0a * (uint)(uVar2 % 0x15),DAT_0061bc08,
                      DAT_0061bc0a);
  local_8 = 0x4b503f;
  FUN__text__0056ce80();
  return;
}

