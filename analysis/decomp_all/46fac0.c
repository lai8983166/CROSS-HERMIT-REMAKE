
void __thiscall FUN__text__0046fac0(int param_1,int param_2,int param_3)

{
  int iVar1;
  uint uVar2;
  undefined4 *puVar3;
  undefined4 local_70 [16];
  undefined2 local_30;
  undefined2 local_2c;
  undefined2 local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar3 = local_70;
  for (iVar1 = 0x1b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_2 == 0) {
    local_c = *(undefined2 *)(DAT_007a49fc + 0x196c);
    local_10 = *(undefined2 *)(DAT_007a49fc + 0x1970);
    local_14 = *(short *)(&DAT_00617ef0 + param_3 * 4);
    local_18 = *(short *)(&DAT_00617ef2 + param_3 * 4);
    local_1c = local_14 + 0x32;
    local_20 = local_18 + 0x37;
  }
  else {
    local_2c = 0x19;
    local_30 = 0x1c;
    local_24 = *(short *)(&DAT_00617ef0 + param_3 * 4) + 0x19;
    uVar2 = (int)*(short *)(&DAT_00617ef2 + param_3 * 4) + 0x1c;
    local_28 = (undefined2)uVar2;
    local_8 = param_1;
    FUN__text__0046fff0(*(undefined2 *)(param_1 + 0x2a330),*(undefined2 *)(param_1 + 0x2a334),
                        *(undefined2 *)(param_1 + 0x2a338),*(undefined2 *)(param_1 + 0x2a33c),
                        local_24,uVar2 & 0xffff,CONCAT22((short)(uVar2 >> 0x10),0x19),0x1c);
  }
  local_8 = 0x46fc13;
  FUN__text__0056ce80();
  return;
}

