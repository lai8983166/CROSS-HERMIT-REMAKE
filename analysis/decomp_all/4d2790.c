
void FUN__text__004d2790(undefined1 *param_1,undefined1 param_2,undefined4 param_3,
                        undefined2 param_4,undefined2 param_5,short param_6,short param_7)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar4 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar1 = (undefined2)((uint)param_1 >> 0x10);
  uVar3 = CONCAT22(uVar1,param_5);
  FUN__text__004d29e0(*param_1,*(undefined2 *)(param_1 + 2),
                      CONCAT31((int3)((uint)uVar3 >> 8),param_2),param_3,
                      CONCAT22((short)((uint)*(ushort *)(param_1 + 4) + (int)param_6 >> 0x10),
                               param_4),uVar3,(uint)*(ushort *)(param_1 + 4) + (int)param_6,
                      (uint)*(ushort *)(param_1 + 6) + (int)param_7,
                      CONCAT22(uVar1,*(undefined2 *)(param_1 + 8)),*(undefined2 *)(param_1 + 10),100
                      ,100,0xff,0x80,0x80,0x80);
  local_8 = 0x4d282a;
  FUN__text__0056ce80();
  return;
}

