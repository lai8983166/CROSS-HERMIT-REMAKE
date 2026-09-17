
void __thiscall FUN__text__0044b170(int param_1,int param_2)

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
  local_14 = param_2;
  if ((-1 < param_2) && (param_2 < 4)) {
    *(undefined1 *)(param_1 + 0x9c) = 0x80;
    *(undefined1 *)(param_1 + 0x9d) = 0x80;
    *(undefined1 *)(param_1 + 0x9e) = 0x80;
    *(undefined1 *)(param_1 + 0x9f) = 0x80;
    local_c = *(undefined2 *)(&DAT_00606498 + param_2 * 8);
    local_10 = *(undefined2 *)(&DAT_0060649a + param_2 * 8);
    local_8 = param_1;
    FUN__text__0044cb40(param_1 + 0x38,local_c,local_10,0x55,5,&DAT_00606558 + param_2 * 8);
  }
  local_8 = 0x44b220;
  FUN__text__0056ce80();
  return;
}

