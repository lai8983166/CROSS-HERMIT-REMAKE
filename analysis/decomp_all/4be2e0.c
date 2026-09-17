
void __thiscall
FUN__text__004be2e0(int param_1,short param_2,short param_3,short param_4,int param_5,short param_6,
                   short param_7,short param_8)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined4 *puVar2;
  undefined4 local_90 [16];
  int local_50;
  short local_4c;
  short local_48;
  ushort local_44;
  short local_40;
  short local_3c;
  ushort local_38;
  short local_34;
  short local_30;
  short local_2c;
  uint local_28;
  short *local_24;
  undefined *local_20;
  short local_1c;
  undefined2 local_18;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_90;
  for (iVar1 = 0x23; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_2 * 0xc6 + 0xe7;
  local_10 = param_3 * 0x8a + 0x27;
  local_14 = param_4;
  local_18 = 0;
  local_1c = 0x57;
  local_20 = &DAT_007e17e8 + param_4 * 0x4a0;
  local_24 = (short *)(param_1 + 0x38 + param_4 * 0x44);
  local_28 = CONCAT22(local_28._2_2_,
                      (ushort)(byte)(&DAT_006b2d8a)
                                    [*(short *)(&DAT_007e17ee + param_4 * 0x4a0) * 0x40]);
  local_30 = param_2 * 7 + param_3 * 0x1c;
  local_34 = param_2 + 0x8c + param_3 * 4;
  local_8 = param_1;
  for (local_2c = 0; local_2c < 7; local_2c = local_2c + 1) {
    local_38 = (ushort)(byte)local_20[local_2c * 8 + 0xc];
    local_3c = local_24[local_2c + 1];
    local_40 = local_38 - local_3c;
    if (param_6 < local_40) {
      local_40 = param_6;
    }
    FUN__text__004d1ec0(local_c + 0x9e,local_10 + 10 + local_2c * 0x12,0,0x10,3,0x57,
                        (int)local_3c + (int)local_40,6,1,2,5,0,&DAT_0061c710);
    if (local_40 != local_24[local_2c + 0x12]) {
      FUN__text__00409ff0(local_8 + 0x1484 + ((int)local_30 + (int)local_2c) * 0x58,0,2,0);
    }
    local_24[local_2c + 0x12] = local_40;
    if (0 < local_40) {
      FUN__text__0040a100(local_8 + 0x1484 + ((int)local_30 + (int)local_2c) * 0x58);
      FUN__text__0040a330(local_8 + 0x1484 + ((int)local_30 + (int)local_2c) * 0x58,local_8 + 0x4ef4
                          ,local_c + 0xb4,local_10 + 0xf + local_2c * 0x12,0);
      FUN__text__004d2700(&DAT_0061c6f0,1,(int)local_1c,local_c + 0xa3,
                          local_10 + 10 + local_2c * 0x12);
      FUN__text__004d1ec0(local_c + 0xb9,local_10 + 10 + local_2c * 0x12,0,0,3,0x57,(int)local_40,6,
                          1,2,5,0,&DAT_0061c710);
    }
    if (param_8 == 0) {
      local_24[local_2c + 0x1a] = 0;
    }
    else if (local_24[local_2c + 9] != 0) {
      if (local_24[local_2c + 0x1a] == 0) {
        local_24[local_2c + 0x1a] = 1;
        FUN__text__00409ff0(local_8 + 0x1484 + ((int)local_30 + (int)local_2c) * 0x58,0,1,0);
      }
      FUN__text__0040a100(local_8 + 0x1484 + ((int)local_30 + (int)local_2c) * 0x58);
      FUN__text__0040a330(local_8 + 0x1484 + ((int)local_30 + (int)local_2c) * 0x58,local_8 + 0x4ef4
                          ,local_c + 0x66,local_10 + 0x13 + local_2c * 0x12,0);
      FUN__text__004d2700(&DAT_0061c6d0,1,(int)local_1c,local_c + 0x5c,
                          local_10 + 9 + local_2c * 0x12);
    }
  }
  local_44 = (ushort)(byte)local_20[0x50];
  local_48 = *local_24;
  local_4c = local_44 - local_48;
  if (param_7 < local_4c) {
    local_4c = param_7;
  }
  if (local_4c != local_24[0x11]) {
    FUN__text__00409ff0(local_8 + 0x1484 + local_34 * 0x58,0,3,0);
  }
  local_24[0x11] = local_4c;
  FUN__text__004d1ec0(local_c + 0x50,local_10 + 0x66,0,0,2,local_1c,(int)local_48 + (int)local_4c,5,
                      1,2,5,0,&DAT_0061c720);
  if (0 < local_4c) {
    FUN__text__0040a100(local_8 + 0x1484 + local_34 * 0x58);
    FUN__text__0040a330(local_8 + 0x1484 + local_34 * 0x58,local_8 + 0x4ef4,local_c + 0x2c,
                        local_10 + 0x29,0);
  }
  iVar1 = *(int *)(&DAT_007cf36c + local_14 * 0x124);
  local_50 = iVar1;
  if (param_5 < iVar1) {
    local_50 = param_5;
  }
  FUN__text__004bef20(local_c + 0x40,local_10 + 0x78,0,0,6,
                      CONCAT22((short)((uint)iVar1 >> 0x10),local_1c),local_50,5,1,3,7,0,
                      &DAT_0061c720,&DAT_0061c780);
  FUN__text__004bf6c0(local_c + 7,local_10 + 3,local_18,local_14 + -1,0xffffffff,0xff,
                      CONCAT22(extraout_var,local_1c));
  FUN__text__004bf870(local_c + 0xd,local_10 + 0x4e,CONCAT22(extraout_var_00,local_18),local_14 + -1
                      ,0xff,CONCAT22(extraout_var_01,local_1c));
  FUN__text__004d2700(&DAT_0061c680,1,(int)local_1c,local_c + 0x65,local_10 + 7);
  FUN__text__004d2790(&DAT_0061c690,1,(int)local_1c,local_c + 0xe,local_10 + 0x65,0,
                      ((local_28 & 0xffff) - 1) * 0xc);
  FUN__text__004d2700(&DAT_0061c6e0,1,(int)local_1c,local_c + 0x43,local_10 + 0x78);
  local_8 = 0x4be93e;
  FUN__text__0056ce80();
  return;
}

