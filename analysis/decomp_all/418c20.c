
void FUN__text__00418c20(int *param_1,undefined4 param_2,uint param_3,int *param_4)

{
  code *pcVar1;
  int iVar2;
  int *piVar3;
  undefined4 *puVar4;
  int *piVar5;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int *local_18;
  int *local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar4 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_4;
  if ((param_3 & 1) == 0) {
    for (local_c = 0; local_c != *local_8; local_c = local_c + 1) {
      local_14 = local_8 + local_c * 0x15 + 3;
      iVar2 = FUN__text__00418f30(local_14 + 6,param_1 + 6);
      if ((iVar2 != 0) && (iVar2 = FUN__text__00418ef0(local_14 + 2,param_1 + 2), iVar2 != 0)) {
        (*API_KERNEL32_DLL_lstrcmpA)(local_14[0xc],param_1[0xc]);
        iVar2 = FUN__text__0056ce80();
        if (iVar2 == 0) goto LAB__text__00418edc;
      }
    }
    if (*local_8 < 0x40) {
      local_18 = local_8 + *local_8 * 0x15 + 3;
      if ((local_18[0xc] != 0) &&
         (iVar2 = FUN__text__00424f80("set->desc.lpszSessionNameA==0",
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff558 + 0x1b,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      if ((local_18[0xd] != 0) &&
         (iVar2 = FUN__text__00424f80("set->desc.lpszPasswordA==0",
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff558 + 0x1c,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      piVar3 = param_1;
      piVar5 = local_18;
      for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
        *piVar5 = *piVar3;
        piVar3 = piVar3 + 1;
        piVar5 = piVar5 + 1;
      }
      if (param_1[0xc] != 0) {
        (*API_KERNEL32_DLL_lstrlenA)(param_1[0xc]);
        local_10 = FUN__text__0056ce80();
        local_10 = local_10 + 2;
        local_1c = FUN__text__00428a40(local_10);
        local_18[0xc] = local_1c;
        if (local_18[0xc] == 0) {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff558 + 0x23,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        else {
          (*API_KERNEL32_DLL_lstrcpyA)(local_18[0xc],param_1[0xc]);
          FUN__text__0056ce80();
        }
      }
      if (param_1[0xd] != 0) {
        (*API_KERNEL32_DLL_lstrlenA)(param_1[0xd]);
        local_10 = FUN__text__0056ce80();
        local_10 = local_10 + 2;
        local_20 = FUN__text__00428a40(local_10);
        local_18[0xd] = local_20;
        if (local_18[0xd] == 0) {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff558 + 0x2a,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        else {
          (*API_KERNEL32_DLL_lstrcpyA)(local_18[0xd],param_1[0xd]);
          FUN__text__0056ce80();
        }
      }
      if ((local_18[0x14] != 0) &&
         (iVar2 = FUN__text__00424f80("set->lpSessionName==0",
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff558 + 0x2d,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      *local_8 = *local_8 + 1;
    }
  }
  else {
    param_4[2] = 1;
  }
LAB__text__00418edc:
  local_8 = (int *)0x418ee9;
  FUN__text__0056ce80();
  return;
}

