
void __fastcall
FUN__text__004d28c0(undefined4 param_1,undefined4 param_2,undefined1 *param_3,undefined1 param_4,
                   undefined4 param_5,undefined2 param_6,undefined2 param_7,undefined2 param_8,
                   undefined2 param_9,undefined2 param_10,undefined2 param_11,undefined1 param_12)

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
  uVar3 = (undefined2)((uint)param_2 >> 0x10);
  uVar2 = CONCAT22(uVar3,param_7);
  FUN__text__004d29e0(*param_3,*(undefined2 *)(param_3 + 2),
                      CONCAT31((int3)((uint)uVar2 >> 8),param_4),param_5,CONCAT22(0xcccc,param_6),
                      uVar2,param_8,CONCAT22(0xcccc,param_9),CONCAT22(uVar3,param_10),param_11,100,
                      100,CONCAT31(0xcccccc,param_12),0x80,0x80,0x80);
  local_8 = 0x4d293d;
  FUN__text__0056ce80();
  return;
}

