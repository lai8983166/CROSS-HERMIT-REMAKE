
void FUN__text__00449380(void)

{
  int iVar1;
  undefined2 extraout_var;
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
  iVar1 = FUN__text__00419450();
  if (iVar1 == 0) {
    local_14 = FUN__text__0041ade0();
    if ((local_14 != 0) && (*(char *)(local_14 + 1) != '\0')) {
      local_c = DAT_00605d28;
      local_10 = DAT_00605d2a;
      FUN__text__0044cb40(local_8 + 0x38,CONCAT22(extraout_var,DAT_00605d28),
                          CONCAT22(*(char *)(local_14 + 1) >> 7,DAT_00605d2a),0x55,5,&DAT_00605d58);
    }
    FUN__text__00410310(0x233,0x2d5,0x1c4,0x23,0x55,0xa0000000,1);
  }
  else {
    FUN__text__00410310(6,0x2dc,0xfa,0x1d,0x55,0xa0000000,1);
  }
  local_8 = 0x449473;
  FUN__text__0056ce80();
  return;
}

