
void FUN__text__00419780(char *param_1)

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
  char local_c [4];
  int local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = (char  [4])s_DefPlayerName_00592f40._0_4_;
  local_14 = (char  [4])s_DefPlayerName_00592f40._4_4_;
  local_10 = (char  [4])s_DefPlayerName_00592f40._8_4_;
  local_c._0_2_ = s_DefPlayerName_00592f40._12_2_;
  FUN__text__004198b0();
  if (param_1 != (char *)0x0) {
    (*API_KERNEL32_DLL_lstrlenA)(param_1);
    local_1c = FUN__text__0056ce80();
    if (local_1c != 0) goto LAB__text__0041980c;
  }
  (*API_KERNEL32_DLL_lstrlenA)(local_18);
  local_1c = FUN__text__0056ce80();
  param_1 = local_18;
LAB__text__0041980c:
  local_20 = FUN__text__00428a40(local_1c + 3);
  *(undefined4 *)(local_8 + 0x1764) = local_20;
  if ((*(int *)(local_8 + 0x1764) == 0) &&
     (iVar2 = FUN__text__00424f80("PlayerName!=0",
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff56c + 0x12,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x1764) != 0) {
    (*API_KERNEL32_DLL_lstrcpyA)(*(undefined4 *)(local_8 + 0x1764),param_1);
    FUN__text__0056ce80();
  }
  local_8 = 0x4198a0;
  FUN__text__0056ce80();
  return;
}

