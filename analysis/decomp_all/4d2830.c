
void __thiscall
FUN__text__004d2830(undefined4 param_1,undefined1 *param_2,undefined1 param_3,undefined4 param_4,
                   undefined2 param_5,undefined2 param_6,undefined2 param_7,undefined2 param_8,
                   undefined2 param_9,undefined2 param_10)

{
  int iVar1;
  undefined2 uVar3;
  undefined4 uVar2;
  undefined4 *puVar4;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar4 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar3 = (undefined2)((uint)param_1 >> 0x10);
  uVar2 = CONCAT22(uVar3,param_6);
  local_8 = param_1;
  FUN__text__004d29e0(*param_2,*(undefined2 *)(param_2 + 2),
                      CONCAT31((int3)((uint)uVar2 >> 8),param_3),param_4,param_5,uVar2,
                      CONCAT22(0xcccc,param_7),param_8,CONCAT22(uVar3,param_9),
                      CONCAT22(0xcccc,param_10),100,100,0xff,0x80,0x80,0x80);
  local_8 = 0x4d28ae;
  FUN__text__0056ce80();
  return;
}

