
void FUN__text__004184a0(undefined4 param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_a4 [16];
  int local_64;
  int local_60;
  undefined4 local_5c;
  int local_58;
  int local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined *local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  int local_28;
  int local_24;
  undefined4 uStack_c;
  int local_8;
  
  puVar3 = local_a4;
  for (iVar2 = 0x28; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__00418720();
  (*API_KERNEL32_DLL_lstrlenA)(param_1);
  iVar2 = FUN__text__0056ce80();
  if (iVar2 < 0xfb) {
    _memset((void *)(local_8 + 0xc),0,0x100);
    (*API_KERNEL32_DLL_lstrcpyA)(local_8 + 0xc,param_1);
    FUN__text__0056ce80();
    _memset(&local_50,0,0x48);
    local_50 = DAT_005cbd2c;
    local_4c = DAT_005cbd30;
    local_48 = DAT_005cbd34;
    local_44 = DAT_005cbd38;
    local_40 = 0x10;
    local_3c = &DAT_005cbe2c;
    local_38 = DAT_005cbccc;
    local_34 = DAT_005cbcd0;
    local_30 = DAT_005cbcd4;
    local_2c = DAT_005cbcd8;
    (*API_KERNEL32_DLL_lstrlenA)(local_8 + 0xc);
    local_28 = FUN__text__0056ce80();
    local_28 = local_28 + 1;
    local_24 = local_8 + 0xc;
    local_54 = 0;
    (**(code **)(**(int **)(local_8 + 4) + 0x38))
              (*(undefined4 *)(local_8 + 4),&local_50,2,0,&local_54);
    local_60 = FUN__text__0056ce80();
    local_58 = local_60;
    if (local_60 == -0x7788ffe2) {
      if ((local_54 == 0) &&
         (iVar2 = FUN__text__00424f80("0<wsize",
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff554 + 0x1e,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_5c = FUN__text__00428a40(local_54);
      *(undefined4 *)(local_8 + 8) = local_5c;
      if ((*(int *)(local_8 + 8) == 0) &&
         (iVar2 = FUN__text__00424f80("DxPlayAddr != 0",
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff554 + 0x26,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if (*(int *)(local_8 + 8) != 0) {
        (**(code **)(**(int **)(local_8 + 4) + 0x38))
                  (*(undefined4 *)(local_8 + 4),&local_50,2,*(undefined4 *)(local_8 + 8),&local_54);
        local_64 = FUN__text__0056ce80();
        local_58 = local_64;
        if (local_64 != 0) {
          FUN__text__0041b4a0(local_64);
        }
      }
    }
    else {
      FUN__text__0041b4a0(local_60);
    }
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                DAT_005ff554 + 0xb,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  uStack_c = 0x41870f;
  FUN__text__0056ce80();
  return;
}

