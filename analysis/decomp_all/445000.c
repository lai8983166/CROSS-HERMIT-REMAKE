
void __thiscall FUN__text__00445000(int param_1,int param_2,undefined1 param_3)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0x200 - DAT_00605a8c / 2;
  local_10 = 0x180 - DAT_00605a8e / 2;
  *(undefined4 *)(param_1 + 0x94) = 0;
  *(undefined1 *)(param_1 + 0x9f) = param_3;
  *(undefined1 *)(param_1 + 0x9c) = 0x80;
  *(undefined1 *)(param_1 + 0x9d) = 0x80;
  *(undefined1 *)(param_1 + 0x9e) = 0x80;
  local_8 = param_1;
  FUN__text__0044cb40(param_1 + 0x38,local_c,local_10,0x5a,2,&DAT_00605a88);
  local_14 = param_2;
  if (param_2 == 0) {
    FUN__text__0044cb40(local_8 + 0x38,CONCAT22(extraout_var,local_c),local_10 + 0x20,0x55,2,
                        &DAT_00605a90);
  }
  else if (param_2 == 1) {
    FUN__text__0044cb40(local_8 + 0x38,CONCAT22(extraout_var,local_c),local_10 + 0x43,0x55,2,
                        &DAT_00605a98);
  }
  else if (param_2 == 2) {
    FUN__text__0044cb40(local_8 + 0x38,CONCAT22(extraout_var,local_c),local_10 + 100,0x55,2,
                        &DAT_00605aa0);
  }
  local_8 = 0x44513e;
  FUN__text__0056ce80();
  return;
}

