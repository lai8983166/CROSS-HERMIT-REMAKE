
void __thiscall FUN__text__00446340(int param_1,undefined4 param_2,undefined1 param_3)

{
  int iVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0x200 - DAT_00605b74 / 2;
  local_10 = 0x180 - DAT_00605b76 / 2;
  *(undefined4 *)(param_1 + 0x94) = 0;
  *(undefined1 *)(param_1 + 0x9f) = param_3;
  *(undefined1 *)(param_1 + 0x9c) = 0x80;
  *(undefined1 *)(param_1 + 0x9d) = 0x80;
  *(undefined1 *)(param_1 + 0x9e) = 0x80;
  local_8 = param_1;
  FUN__text__0044cb40(param_1 + 0x38,local_c,local_10,0x5a,3,&DAT_00605b70);
  local_14 = param_2;
  uVar2 = extraout_var;
  switch(param_2) {
  case 0:
    FUN__text__0044cb40(local_8 + 0x38,local_c,local_10 + 0xd8,0x55,3,&DAT_00605b78);
    uVar2 = extraout_var_00;
    break;
  case 1:
    FUN__text__0044cb40(local_8 + 0x38,local_c + 0x7f,local_10 + 0xd8,0x55,3,&DAT_00605b80);
    uVar2 = extraout_var_01;
    break;
  case 2:
    FUN__text__0044cb40(local_8 + 0x38,local_c,local_10 + 0xff,0x55,3,&DAT_00605b88);
    uVar2 = extraout_var_02;
    break;
  case 3:
    FUN__text__0044cb40(local_8 + 0x38,local_c,local_10 + 0x126,0x55,3,&DAT_00605b90);
    uVar2 = extraout_var_03;
    break;
  case 4:
    FUN__text__0044cb40(local_8 + 0x38,local_c + 0xe6,local_10 + 0x49,0x55,3,&DAT_00605b98);
    uVar2 = extraout_var_04;
    break;
  case 5:
    FUN__text__0044cb40(local_8 + 0x38,local_c + 0xe6,local_10 + 0x6b,0x55,3,&DAT_00605ba0);
    uVar2 = extraout_var_05;
    break;
  case 6:
    FUN__text__0044cb40(local_8 + 0x38,local_c + 0xe6,local_10 + 0x8d,0x55,3,&DAT_00605ba8);
    uVar2 = extraout_var_06;
    break;
  case 7:
    FUN__text__0044cb40(local_8 + 0x38,local_c + 0xe6,local_10 + 0xaf,0x55,3,&DAT_00605bb0);
    uVar2 = extraout_var_07;
  }
  FUN__text__004465c0(CONCAT22(uVar2,local_c),local_10,param_3);
  FUN__text__0044d1d0();
  local_8 = 0x446597;
  FUN__text__0056ce80();
  return;
}

