
void FUN__text__004d2950(undefined1 *param_1,undefined1 param_2,undefined4 param_3,
                        undefined2 param_4,undefined2 param_5,undefined1 param_6)

{
  int iVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar2 = (undefined2)((uint)param_1 >> 0x10);
  FUN__text__004d29e0(*param_1,*(undefined2 *)(param_1 + 2),
                      CONCAT31((int3)(CONCAT22(uVar2,param_5) >> 8),param_2),param_3,
                      CONCAT22(uVar2,param_4),CONCAT22(uVar2,param_5),
                      CONCAT22(uVar2,*(undefined2 *)(param_1 + 4)),
                      CONCAT22(uVar2,*(undefined2 *)(param_1 + 6)),
                      CONCAT22(uVar2,*(undefined2 *)(param_1 + 8)),*(undefined2 *)(param_1 + 10),100
                      ,100,CONCAT31(0xcccccc,param_6),0x80,0x80,0x80);
  local_8 = 0x4d29d9;
  FUN__text__0056ce80();
  return;
}

