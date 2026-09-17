
void __fastcall FUN__text__004483c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x94) = 0;
  *(undefined1 *)(param_1 + 0x9f) = 0xff;
  *(undefined1 *)(param_1 + 0x9c) = 0x80;
  *(undefined1 *)(param_1 + 0x9d) = 0x80;
  *(undefined1 *)(param_1 + 0x9e) = 0x80;
  local_8 = param_1;
  if (*(char *)(param_1 + 0x1aa2) == '\0') {
    FUN__text__0044cb40(param_1 + 0x38,DAT_00605cf8,PTR_DAT_00605cfa._0_2_,0x55,5,&DAT_00605d08);
  }
  else {
    FUN__text__0044cb40(param_1 + 0x38,DAT_00605d00,PTR_DAT_00605d02._0_2_,0x55,5,&DAT_00605d10);
  }
  local_8 = 0x44847f;
  FUN__text__0056ce80();
  return;
}

