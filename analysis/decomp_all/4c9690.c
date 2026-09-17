
void __thiscall
FUN__text__004c9690(int param_1,short param_2,short param_3,undefined2 param_4,uint param_5,
                   undefined2 param_6)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  uint local_14;
  undefined2 local_10;
  undefined2 uStack_e;
  undefined2 local_c;
  undefined2 uStack_a;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = (uint)*(ushort *)(param_1 + 0x30);
  local_8 = param_1;
  if (local_14 == 0) {
    uVar1 = *(undefined2 *)(param_1 + 0x40 + (param_5 & 0xff) * 2);
    _local_10 = CONCAT22(uStack_e,uVar1);
    FUN__text__004cbdb0((int)param_2,(int)param_3,param_4,0xffffffff,param_6,0,0,0x100,0x128,uVar1,0
                       );
  }
  else if (local_14 == 1) {
    uVar1 = *(undefined2 *)(param_1 + 0x40 + (param_5 & 0xff) * 2);
    _local_c = CONCAT22(uStack_a,uVar1);
    FUN__text__004cbdb0((int)param_2,(int)param_3,param_4,0xffffffff,param_6,0,0,0x200,0x300,uVar1,0
                       );
  }
  local_8 = 0x4c978b;
  FUN__text__0056ce80();
  return;
}

