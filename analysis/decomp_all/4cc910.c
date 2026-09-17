
void __thiscall FUN__text__004cc910(int param_1,int param_2,int param_3)

{
  undefined2 extraout_var;
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
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
  local_14 = *(ushort *)(local_10 + 2) - 2;
  switch(local_14) {
  case 0:
  case 1:
  case 3:
  case 4:
    local_8 = param_1;
    FUN__text__004ca0b0(0x2d);
    FUN__text__004ca0f0(CONCAT22(extraout_var,(undefined2)param_3));
    if (param_3 == 0) {
      FUN__text__004ca130(4,0,0xffffffff,0xffffffff);
    }
    else {
      FUN__text__004ca130(7,0,0xffffffff,0xffffffff);
    }
  }
  local_8 = 0x4cc9cb;
  FUN__text__0056ce80();
  return;
}

