
void __thiscall FUN__text__00431a60(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  char local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((param_2 < 0) || (0xf < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=player) && (player<16)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                  DAT_005ff740 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  for (local_c = 0; local_c != 4; local_c = local_c + 1) {
    local_10 = *(char *)(local_8 + 0x115aac + local_c + param_2 * 0x10);
    if (local_10 == '\0') goto LAB__text__00431b1b;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp"
                              ,DAT_005ff740 + 0x10,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
LAB__text__00431b1b:
  local_8 = 0x431b28;
  FUN__text__0056ce80();
  return;
}

