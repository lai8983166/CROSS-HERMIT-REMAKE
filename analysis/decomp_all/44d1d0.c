
void __fastcall FUN__text__0044d1d0(int param_1)

{
  int iVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 local_94 [16];
  undefined2 local_54;
  undefined2 uStack_52;
  undefined2 local_50;
  undefined2 uStack_4e;
  uint local_4c;
  undefined1 local_48 [64];
  int local_8;
  
  puVar3 = local_94;
  for (iVar1 = 0x24; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_4c = *(uint *)(param_1 + 0x34);
  uVar2 = (undefined2)(local_4c >> 0x10);
  _local_50 = CONCAT22(uStack_4e,uVar2);
  _local_54 = CONCAT22(uStack_52,(short)local_4c);
  local_8 = param_1;
  FUN__text__0056d810(local_48,"VERSION %2d.%2d",uVar2,local_4c & 0xffff);
  FUN__text__0040ec50(0x374,0x2e4,0x55,0xff6060a0,0,local_48);
  local_8 = 0x44d275;
  FUN__text__0056ce80();
  return;
}

