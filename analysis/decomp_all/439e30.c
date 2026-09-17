
void __thiscall FUN__text__00439e30(int param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [14];
  undefined4 uStack_10;
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x1c) == 1) {
    FUN__text__0042b2d0(&DAT_00595524);
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\GameCtrl.cpp",
                                DAT_005ff9c8 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_NTDLL_DLL_RtlEnterCriticalSection)(local_8 + 4);
  FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x20) = param_2;
  *(undefined4 *)(local_8 + 0x1c) = 1;
  (*API_NTDLL_DLL_RtlLeaveCriticalSection)(local_8 + 4);
  FUN__text__0056ce80();
  uStack_10 = 0x439ede;
  FUN__text__0056ce80();
  return;
}

