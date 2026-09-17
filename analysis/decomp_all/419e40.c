
void FUN__text__00419e40(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [15];
  undefined4 uStack_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__00419f00();
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  local_c = FUN__text__0056ce80();
  local_10 = FUN__text__00428a40(param_2 + 1);
  *(undefined4 *)(local_8 + 0x177c) = local_10;
  if (*(int *)(local_8 + 0x177c) == 0) {
    iVar2 = FUN__text__00424f80("IpAddrString",
                                "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                DAT_005ff574 + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_KERNEL32_DLL_lstrcpyA)(*(undefined4 *)(local_8 + 0x177c),param_1);
  FUN__text__0056ce80();
  uStack_14 = 0x419ef3;
  FUN__text__0056ce80();
  return;
}

