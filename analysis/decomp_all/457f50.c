
void FUN__text__00457f50(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  char local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_1 + 8);
  iVar2 = FUN__text__00419450();
  if (iVar2 != 0) {
    FUN__text__00457e00(*(undefined1 *)(local_c + 0x10),*(undefined1 *)(local_c + 0x11),
                        local_c + 0x12);
  }
  local_10 = FUN__text__0041ad60();
  if ((local_10 == -1) &&
     (iVar2 = FUN__text__00424f80("player_no != -1",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                  DAT_0060cdd4 + 0x11,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(char *)(local_c + 0x10) != local_10) &&
     ((*(char *)(local_c + 0x11) == -1 ||
      (iVar2 = FUN__text__00458060(CONCAT31(*(char *)(local_c + 0x11) >> 7,
                                            *(undefined1 *)(local_c + 0x10))), iVar2 != 0)))) {
    FUN__text__004254c0(local_c + 0x12);
  }
  local_8 = 0x45804b;
  FUN__text__0056ce80();
  return;
}

