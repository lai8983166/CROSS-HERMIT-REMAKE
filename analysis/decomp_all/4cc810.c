
void __thiscall FUN__text__004cc810(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  uint local_14;
  int local_10;
  short *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (short *)(&DAT_00624520 + param_2 * 0x26);
  local_10 = param_1 + 0x6f60 + *local_c * 0xe0;
  local_14 = (uint)*(ushort *)(local_10 + 2);
  if (((local_14 == 1) || (local_14 == 4)) || (local_14 == 7)) {
    local_8 = param_1;
    FUN__text__004ca0b0(0x2d);
    FUN__text__004ca0f0(CONCAT22(extraout_var,(undefined2)param_3));
    if (param_3 == 0) {
      FUN__text__004ca130(3,0,0xffffffff,0xffffffff);
    }
    else {
      FUN__text__004ca130(6,0,0xffffffff,0xffffffff);
    }
  }
  local_8 = 0x4cc8c6;
  FUN__text__0056ce80();
  return;
}

