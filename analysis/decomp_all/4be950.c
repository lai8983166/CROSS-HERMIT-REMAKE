
void FUN__text__004be950(short param_1,short param_2)

{
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  int iVar1;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined4 *puVar2;
  undefined4 local_6c [16];
  int local_2c;
  short local_28;
  short local_24;
  short local_20;
  undefined2 local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 1;
  local_10 = param_1 * 0x8a + 0x27;
  local_14 = 0x57;
  local_18 = param_2 + -0x65;
  local_1c = 1;
  local_20 = *(short *)(&DAT_007a529a + param_1 * 0x70);
  iVar1 = 7 - *(short *)(&DAT_007a529e + param_1 * 0x70);
  local_24 = (short)iVar1;
  local_28 = 0;
  local_2c = (int)local_20;
  if (local_2c == 2) {
    local_28 = 1;
    FUN__text__004beb90(0x2a,local_10 + 0x68,
                        CONCAT22((short)((uint)(param_1 * 0x70) >> 0x10),
                                 *(undefined2 *)(&DAT_007a52a0 + param_1 * 0x70)),
                        CONCAT22(local_20 >> 0xf,*(undefined2 *)(&DAT_007a52a2 + param_1 * 0x70)),1,
                        0,0xff,CONCAT22(*(short *)(&DAT_007a529e + param_1 * 0x70) >> 0xf,0x57));
  }
  else if (local_2c == 4) {
    local_28 = 0;
    FUN__text__004bee00(0x2a,local_10 + 0x68,
                        CONCAT22((short)((uint)(param_1 * 0x70) >> 0x10),
                                 *(undefined2 *)(&DAT_007a52a0 + param_1 * 0x70)),
                        CONCAT22((short)((uint)iVar1 >> 0x10),
                                 *(undefined2 *)(&DAT_007a52a2 + param_1 * 0x70)),0xff,
                        CONCAT22(local_20 >> 0xf,0x57));
  }
  FUN__text__004d2790(&DAT_0061c6b0,1,(int)local_14,local_c + 0x7a,local_10 + 0x2d,0,local_28 * 0xc)
  ;
  FUN__text__004bf6c0(local_c + 7,local_10 + 3,CONCAT22(extraout_var,local_1c),
                      CONCAT22(extraout_var_03,local_18),0xffffffff,0xff,
                      CONCAT22(extraout_var_01,local_14));
  FUN__text__004bf870(local_c + 0xd,local_10 + 0x4e,CONCAT22(extraout_var_04,local_1c),
                      CONCAT22(extraout_var_02,local_18),0xff,CONCAT22(extraout_var_00,local_14));
  FUN__text__004d2700(&DAT_0061c6a0,1,(int)local_14,local_c + 0x7a,local_10 + 10);
  FUN__text__004d2790(&DAT_0061c6c0,1,(int)local_14,local_c + 0x7a,local_10 + 0x3e,0,local_24 * 0xc)
  ;
  local_8 = 0x4beb83;
  FUN__text__0056ce80();
  return;
}

