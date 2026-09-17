
void __fastcall FUN__text__0049c9b0(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined *puVar6;
  undefined4 uVar7;
  undefined4 local_58 [16];
  char local_18;
  int local_14;
  int local_10;
  undefined **local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_18 = *(char *)(param_1 + 0x2f15c);
  local_8 = param_1;
  if (local_18 == '\0') {
    if (((*(char *)(param_1 + 0x2f15e) < '\0') || (0x17 < *(byte *)(param_1 + 0x2f15e))) &&
       (iVar3 = FUN__text__00424f80("(0<=uCtrlp.help_no[0]) && (uCtrlp.help_no[0]<(sizeof(UnitOMH_Param)/(sizeof(sint8*)*4)))"
                                    ,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                    DAT_0061affc + 7,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = &PTR_DAT_0061a4a8 + *(char *)(local_8 + 0x2f15e) * 4;
  }
  else if (local_18 == '\x01') {
    if (((*(char *)(param_1 + 0x2f15e) < '\0') || (0x14 < *(byte *)(param_1 + 0x2f15e))) &&
       (iVar3 = FUN__text__00424f80("(0<=uCtrlp.help_no[0]) && (uCtrlp.help_no[0]<(sizeof(UnitOMH_CtrlPanel)/(sizeof(sint8*)*4)))"
                                    ,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                    DAT_0061affc + 0xb,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = &PTR_DAT_0061a628 + *(char *)(local_8 + 0x2f15e) * 4;
  }
  else if (local_18 == '\x02') {
    if (((*(char *)(param_1 + 0x2f15e) < '\0') || (99 < *(byte *)(param_1 + 0x2f15e))) &&
       (iVar3 = FUN__text__00424f80("(0<=uCtrlp.help_no[0]) && (uCtrlp.help_no[0]<(sizeof(UnitOMH_Skill)/(sizeof(sint8*)*4)))"
                                    ,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                    DAT_0061affc + 0xf,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = &PTR_DAT_0061a778 + *(char *)(local_8 + 0x2f15e) * 4;
  }
  else {
    iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                DAT_0061affc + 0x13,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined1 *)(local_8 + 0x2f161) = 0;
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    (*API_KERNEL32_DLL_lstrlenA)(local_c[local_10]);
    local_14 = FUN__text__0056ce80();
    if (local_14 != 0) {
      FUN__text__004077c0(DAT_007a49fc);
      uVar7 = 0;
      puVar6 = local_c[local_10];
      uVar5 = *(undefined4 *)(local_8 + 0xdb810);
      uVar2 = FUN__text__004142b0(uVar5,puVar6,0);
      FUN__text__00408e30(uVar2,uVar5,puVar6,uVar7);
      *(byte *)(local_8 + 0x2f161) =
           *(byte *)(local_8 + 0x2f161) | (byte)(0x80 >> ((byte)local_10 & 0x1f));
    }
  }
  local_8 = 0x49cbfd;
  FUN__text__0056ce80();
  return;
}

