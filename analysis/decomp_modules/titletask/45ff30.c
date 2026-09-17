
void FUN__text__0045ff30(void)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_94 [16];
  undefined2 local_54;
  undefined2 uStack_52;
  undefined2 local_50;
  undefined2 uStack_4e;
  uint local_4c;
  undefined1 local_48 [64];
  undefined4 local_8;
  
  puVar3 = local_94;
  for (iVar2 = 0x24; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_4c = FUN__text__004e2c30();
  uVar1 = (undefined2)(local_4c >> 0x10);
  _local_50 = CONCAT22(uStack_4e,uVar1);
  _local_54 = CONCAT22(uStack_52,(short)local_4c);
  FUN__text__0056d810(local_48,"VERSION %2d.%2d",uVar1,local_4c & 0xffff);
  FUN__text__0040ec50(0x374,0x2e4,0x51,0xff6060a0,0,local_48);
  local_8 = 0x45ffd3;
  FUN__text__0056ce80();
  return;
}

