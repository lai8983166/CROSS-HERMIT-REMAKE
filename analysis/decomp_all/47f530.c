
void __thiscall
FUN__text__0047f530(int param_1,undefined4 param_2,int param_3,int param_4,undefined4 param_5,
                   undefined4 param_6)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  uint local_18;
  uint local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_3 < 0) || (0xf < param_3)) {
    iVar2 = FUN__text__00424f80("(0<=player)&&(player<=15)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e80 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((param_4 < 0) || (0xff < param_4)) {
    iVar2 = FUN__text__00424f80("(0<=group)&&(group<=255)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e80 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_14 = CONCAT31(local_14._1_3_,(undefined1)param_3);
  local_18 = CONCAT31(local_18._1_3_,(undefined1)param_4);
  local_10 = 0;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar2 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if (((iVar2 != 0) &&
        ((local_14 & 0xff) == (uint)*(byte *)(*(int *)(local_8 + 0x80d44 + local_c * 0x520) + 0xa4))
        ) && ((local_18 & 0xff) ==
              (uint)*(byte *)(*(int *)(local_8 + 0x80d44 + local_c * 0x520) + 0x98))) {
      iVar2 = FUN__text__0047f6b0(param_2,local_8 + 0x80aec + local_c * 0x520,param_5,param_6);
      local_10 = local_10 + iVar2;
    }
  }
  local_8 = 0x47f69b;
  FUN__text__0056ce80();
  return;
}

