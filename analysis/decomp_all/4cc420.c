
void __thiscall FUN__text__004cc420(int param_1,int param_2,int param_3)

{
  undefined2 extraout_var;
  int iVar1;
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
  local_14 = (uint)*(ushort *)(local_10 + 0x22);
  switch(local_14) {
  case 0:
  case 1:
  case 4:
  case 8:
    local_8 = param_1;
    FUN__text__004c9610(0x3c);
    FUN__text__004c9650(CONCAT22(extraout_var,(undefined2)param_3));
    if (param_3 == 0) {
      *(undefined2 *)(local_10 + 0x22) = 3;
      *(undefined2 *)(local_10 + 0x24) = 0;
    }
    else {
      *(undefined2 *)(local_10 + 0x22) = 7;
      *(undefined2 *)(local_10 + 0x24) = 0;
    }
  }
  local_8 = 0x4cc4de;
  FUN__text__0056ce80();
  return;
}

