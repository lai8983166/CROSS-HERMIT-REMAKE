
void __thiscall FUN__text__00446c70(int param_1,undefined4 param_2,undefined1 param_3)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0x200 - DAT_00605bdc / 2;
  local_10 = 0x180 - DAT_00605bde / 2;
  if (*(int *)(param_1 + 0x94) == 0xff) {
    *(undefined4 *)(param_1 + 0x94) = 0;
  }
  else {
    *(undefined4 *)(param_1 + 0x94) = 1;
  }
  *(undefined1 *)(param_1 + 0x9f) = param_3;
  *(undefined1 *)(param_1 + 0x9c) = 0x80;
  *(undefined1 *)(param_1 + 0x9d) = 0x80;
  *(undefined1 *)(param_1 + 0x9e) = 0x80;
  local_8 = param_1;
  FUN__text__0044cb40(param_1 + 0x38,local_c,local_10,0x5a,4,&DAT_00605bd8);
  local_14 = param_2;
  switch(param_2) {
  case 0:
    FUN__text__0044cb40(local_8 + 0x38,local_c,CONCAT22(extraout_var,local_10),0x55,4,&DAT_00605be0)
    ;
    break;
  case 1:
    FUN__text__0044cb40(local_8 + 0x38,local_c,local_10 + 0x71,0x55,4,&DAT_00605be8);
    break;
  case 2:
    FUN__text__0044cb40(local_8 + 0x38,local_c + 6,local_10 + 0x99,0x55,4,&DAT_00605bf0);
    break;
  case 3:
    FUN__text__0044cb40(local_8 + 0x38,local_c + 6,local_10 + 0xc0,0x55,4,&DAT_00605bf8);
  }
  local_8 = 0x446dfc;
  FUN__text__0056ce80();
  return;
}

