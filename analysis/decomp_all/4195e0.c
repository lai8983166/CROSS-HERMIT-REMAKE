
void FUN__text__004195e0(char *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  undefined4 local_20;
  int local_1c;
  char local_18 [4];
  char local_14 [4];
  char local_10 [4];
  char local_c [2];
  char local_a;
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = (char  [4])s_DefSessionName_00592f20._0_4_;
  local_14 = (char  [4])s_DefSessionName_00592f20._4_4_;
  local_10 = (char  [4])s_DefSessionName_00592f20._8_4_;
  local_c = (char  [2])s_DefSessionName_00592f20._12_2_;
  local_a = s_DefSessionName_00592f20[0xe];
  FUN__text__00419710();
  if (param_1 != (char *)0x0) {
    (*API_KERNEL32_DLL_lstrlenA)(param_1);
    local_1c = FUN__text__0056ce80();
    if (local_1c != 0) goto LAB__text__00419675;
  }
  (*API_KERNEL32_DLL_lstrlenA)(local_18);
  local_1c = FUN__text__0056ce80();
  param_1 = local_18;
LAB__text__00419675:
  local_20 = FUN__text__00428a40(local_1c + 3);
  *(undefined4 *)(local_8 + 0x1760) = local_20;
  if ((*(int *)(local_8 + 0x1760) == 0) &&
     (iVar2 = FUN__text__00424f80("SessionName!=0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff568 + 0x12,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x1760) != 0) {
    (*API_KERNEL32_DLL_lstrcpyA)(*(undefined4 *)(local_8 + 0x1760),param_1);
    FUN__text__0056ce80();
  }
  local_8 = 0x419709;
  FUN__text__0056ce80();
  return;
}

