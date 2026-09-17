
void FUN__text__0041afd0(undefined4 param_1,undefined4 param_2)

{
  code *pcVar1;
  undefined1 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_10 = FUN__text__0041acf0();
  if (local_10 < 0x10) {
    local_c = FUN__text__0041ab60();
    if ((local_c == 0) &&
       (iVar3 = FUN__text__00424f80("set != 0",
                                    "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                    DAT_005ff590 + 0xe,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (*API_KERNEL32_DLL_lstrlenA)(param_1);
    local_14 = FUN__text__0056ce80();
    if ((0x7e < local_14) &&
       (iVar3 = FUN__text__00424f80("len < (128-1)",
                                    "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                    DAT_005ff590 + 0x12,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    (*API_KERNEL32_DLL_lstrcpyA)(local_c + 2,param_1);
    FUN__text__0056ce80();
    *(undefined4 *)(local_c + 0x84) = param_2;
    uVar2 = FUN__text__0041acf0();
    *(undefined1 *)(local_8 + 0x2000) = uVar2;
  }
  else {
    iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                DAT_005ff590 + 9,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x41b0e9;
  FUN__text__0056ce80();
  return;
}

