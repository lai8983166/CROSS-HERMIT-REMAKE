
void __thiscall FUN__text__0047fa40(int param_1,undefined4 param_2,int param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  uint local_1c;
  uint local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_3 < 0) || (0xf < param_3)) {
    iVar2 = FUN__text__00424f80("(0<=player)&&(player<=15)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e88 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((param_4 < 0) || (0xff < param_4)) {
    iVar2 = FUN__text__00424f80("(0<=group)&&(group<=255)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e88 + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_18 = CONCAT31(local_18._1_3_,(undefined1)param_3);
  local_1c = CONCAT31(local_1c._1_3_,(undefined1)param_4);
  local_14 = 0;
  for (local_10 = 0; local_10 != 0xfa; local_10 = local_10 + 1) {
    iVar2 = FUN__text__00468d10(local_8 + 0x80aec + local_10 * 0x520);
    if (((iVar2 != 0) &&
        ((local_18 & 0xff) == (uint)*(byte *)(*(int *)(local_8 + 0x80d44 + local_10 * 0x520) + 0xa4)
        )) && ((local_1c & 0xff) ==
               (uint)*(byte *)(*(int *)(local_8 + 0x80d44 + local_10 * 0x520) + 0x98))) {
      local_c = local_8 + 0x80aec + local_10 * 0x520;
      iVar2 = FUN__text__00469220(local_c);
      if (iVar2 != 0) {
        *(undefined1 *)(*(int *)(local_c + 600) + 0xf) = 2;
        *(undefined2 *)(*(int *)(local_c + 600) + 0x16) =
             *(undefined2 *)(*(int *)(local_c + 600) + 0x14);
        *(undefined2 *)(*(int *)(local_c + 600) + 0x1c) =
             *(undefined2 *)(*(int *)(local_c + 600) + 0x1a);
      }
    }
  }
  local_8 = 0x47fbe6;
  FUN__text__0056ce80();
  return;
}

