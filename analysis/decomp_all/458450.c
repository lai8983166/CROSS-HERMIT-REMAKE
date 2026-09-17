
void FUN__text__00458450(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  char local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_1 + 8);
  iVar2 = FUN__text__00419450();
  if (iVar2 != 0) {
    FUN__text__00458380(*(undefined2 *)(local_c + 0x12),*(undefined2 *)(local_c + 0x14),
                        *(undefined1 *)(local_c + 0x10),*(undefined1 *)(local_c + 0x11));
  }
  local_10 = FUN__text__0041ad60();
  if (local_10 == -1) {
    iVar2 = FUN__text__00424f80("player_no != -1",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cddc + 0x11,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if (*(char *)(local_c + 0x10) != local_10) {
    if (*(char *)(local_c + 0x11) == -1) {
      local_14 = 0;
    }
    else {
      iVar2 = FUN__text__00458060(CONCAT31(local_10 >> 7,*(undefined1 *)(local_c + 0x10)));
      if (iVar2 == 0) goto LAB__text__00458559;
      local_14 = 1;
    }
    FUN__text__00493960((int)*(short *)(local_c + 0x12),(int)*(short *)(local_c + 0x14),local_14);
  }
LAB__text__00458559:
  local_8 = 0x45856f;
  FUN__text__0056ce80();
  return;
}

