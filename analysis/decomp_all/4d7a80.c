
void __thiscall FUN__text__004d7a80(int param_1,short param_2)

{
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  int iVar1;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined4 *puVar2;
  undefined4 local_90 [16];
  int local_50;
  undefined2 local_4c;
  undefined2 local_48;
  undefined2 local_44;
  undefined2 local_40;
  undefined2 local_3c;
  undefined2 local_38;
  undefined2 local_34;
  undefined2 local_30;
  undefined2 local_2c;
  undefined2 local_28;
  undefined2 local_24;
  undefined2 local_20;
  undefined2 local_1c;
  undefined2 local_18;
  undefined2 local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar2 = local_90;
  for (iVar1 = 0x23; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_50 = (int)param_2;
  local_8 = param_1;
  switch(local_50) {
  case 0:
    local_10 = 0x17a;
    local_14 = 0x162;
    local_18 = 0x17f;
    local_1c = 0x16c;
    if (*(short *)(param_1 + 0x2c724) != param_2) {
      FUN__text__004d60e0(5);
      FUN__text__004d6150(&DAT_005c831c);
      FUN__text__004d6150(&DAT_005c8304);
    }
    FUN__text__004d62f0(local_18,local_1c,0x53);
    FUN__text__004d68b0(&DAT_006257b8,0x54,CONCAT22(extraout_var_02,local_10),
                        CONCAT22(extraout_var,local_14),1);
    FUN__text__004d2620(0xaa,0xb7,0x2b7,0x1b2,0x55,0xc0101010,1);
    break;
  case 1:
    local_20 = 0x179;
    local_24 = 0x192;
    local_28 = 0x17e;
    local_2c = 0x19c;
    if (*(short *)(param_1 + 0x2c724) != param_2) {
      FUN__text__004d60e0(5);
      FUN__text__004d6150(&DAT_005c831c);
      FUN__text__004d6150(&DAT_005c8304);
    }
    FUN__text__004d62f0(local_28,local_2c,0x53);
    FUN__text__004d68b0(&DAT_006257b8,0x54,CONCAT22(extraout_var_05,local_20),
                        CONCAT22(extraout_var_03,local_24),1);
    FUN__text__004d2620(0xaa,300,0x2b7,0x13d,0x55,0xc0101010,1);
    break;
  case 2:
    local_30 = 0x179;
    local_34 = 0x192;
    local_38 = 0x17e;
    local_3c = 0x19c;
    if (*(short *)(param_1 + 0x2c724) != param_2) {
      FUN__text__004d60e0(5);
      FUN__text__004d6150(&DAT_005c82f8);
      FUN__text__004d6150(&DAT_005c82e4);
      FUN__text__004d6150(&DAT_005c82d0);
    }
    FUN__text__004d62f0(local_38,local_3c,0x53);
    FUN__text__004d68b0(&DAT_006257b8,0x54,CONCAT22(extraout_var_00,local_30),
                        CONCAT22(extraout_var_06,local_34),1);
    FUN__text__004d2620(0xaa,300,0x2b7,0x13d,0x55,0xc0101010,1);
    break;
  case 3:
    local_40 = 0x179;
    local_44 = 0x192;
    local_48 = 0x17e;
    local_4c = 0x19c;
    if (*(short *)(param_1 + 0x2c724) != param_2) {
      FUN__text__004d60e0(5);
      FUN__text__004d6150(&DAT_005c82bc);
      FUN__text__004d6150(&DAT_005c82a8);
    }
    FUN__text__004d62f0(local_48,local_4c,0x53);
    FUN__text__004d68b0(&DAT_006257b8,0x54,CONCAT22(extraout_var_04,local_40),
                        CONCAT22(extraout_var_01,local_44),1);
    FUN__text__004d2620(0xaa,300,0x2b7,0x13d,0x55,0xc0101010,1);
  }
  *(short *)(local_8 + 0x2c724) = param_2;
  local_8 = 0x4d7e5f;
  FUN__text__0056ce80();
  return;
}

