
void __thiscall FUN__text__004cc600(int param_1,int param_2)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
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
  *(undefined2 *)(local_10 + 0x30) = *(undefined2 *)(&DAT_00624528 + param_2 * 0x26);
  local_8 = param_1;
  FUN__text__004c9520();
  FUN__text__004ca060(local_c[1],CONCAT22(extraout_var,local_c[2]));
  FUN__text__004ca960(local_c[7],CONCAT22(extraout_var_00,local_c[8]));
  *(short *)(local_10 + 0x4c) = local_c[0xb];
  *(short *)(local_10 + 0x16) = local_c[0xe];
  *(short *)(local_10 + 0x18) = local_c[0xf];
  *(short *)(local_10 + 0x1a) = local_c[0x10];
  *(short *)(local_10 + 0x1c) = local_c[0x11];
  if (*(short *)(local_10 + 0x4c) == 1) {
    FUN__text__004ca720(local_c[0xc],local_c[0xd]);
  }
  local_14 = (uint)*(ushort *)(local_10 + 2);
  switch(local_14) {
  case 0:
  case 1:
    FUN__text__004ca130(1,0,(char)local_c[0x12],0xffffffff);
    FUN__text__004ca0b0(8);
    break;
  case 2:
    if ((uint)*(ushort *)(local_10 + 8) != (int)*local_c) {
      FUN__text__004ca130(5,0,0xffffffff,(char)local_c[0x12]);
    }
    break;
  case 3:
  case 4:
  case 6:
  case 7:
    FUN__text__004ca130(0xffffffff,0xffffffff,(char)local_c[0x12],0xffffffff);
    break;
  case 5:
    FUN__text__004ca130(0xffffffff,0xffffffff,0xffffffff,(char)local_c[0x12]);
  }
  local_8 = 0x4cc7a2;
  FUN__text__0056ce80();
  return;
}

