
void __thiscall FUN__text__00449d00(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_10 = 0;
  local_14 = param_2;
  local_8 = param_1;
  switch(param_2) {
  case 0:
  case 1:
  case 2:
  case 3:
    local_c = *(undefined2 *)(&DAT_00605d78 + param_2 * 8);
    local_10 = *(undefined2 *)(&DAT_00605d7a + param_2 * 8);
    FUN__text__0044cb40(param_1 + 0x38,local_c,local_10,0x55,5,&DAT_00605e58 + param_2 * 8);
    break;
  case 4:
  case 5:
  case 6:
  case 7:
    local_c = *(undefined2 *)(&DAT_00605d78 + param_2 * 8);
    local_10 = *(undefined2 *)(&DAT_00605d7a + param_2 * 8);
    FUN__text__0044cb40(param_1 + 0x38,local_c,local_10,0x55,5,&DAT_00605e38 + param_2 * 8);
  }
  local_8 = 0x449de6;
  FUN__text__0056ce80();
  return;
}

