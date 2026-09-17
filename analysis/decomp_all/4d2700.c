
void FUN__text__004d2700(undefined1 *param_1,undefined1 param_2,undefined4 param_3,
                        undefined2 param_4,undefined2 param_5)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar1 = (undefined2)((uint)param_1 >> 0x10);
  FUN__text__004d29e0(*param_1,*(undefined2 *)(param_1 + 2),
                      CONCAT31((int3)(CONCAT22(uVar1,param_5) >> 8),param_2),param_3,
                      CONCAT22(uVar1,param_4),CONCAT22(uVar1,param_5),
                      CONCAT22(uVar1,*(undefined2 *)(param_1 + 4)),
                      CONCAT22(uVar1,*(undefined2 *)(param_1 + 6)),
                      CONCAT22(uVar1,*(undefined2 *)(param_1 + 8)),*(undefined2 *)(param_1 + 10),100
                      ,100,0xff,0x80,0x80,0x80);
  local_8 = 0x4d278a;
  FUN__text__0056ce80();
  return;
}

