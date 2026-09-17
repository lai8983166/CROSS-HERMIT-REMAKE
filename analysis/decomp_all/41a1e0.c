
void __thiscall FUN__text__0041a1e0(undefined4 *param_1,int *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 *local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; local_8 = param_1, iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  do {
    _memset(param_2,0,0x10);
    (**(code **)(*(int *)*local_8 + 100))(*local_8,param_2,param_2 + 1,1,0,param_2 + 3);
    local_1c = FUN__text__0056ce80();
    local_c = local_1c;
    if (local_1c != -0x7788ffe2) {
      if ((local_1c != -0x7788ff42) &&
         (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff580 + 0x12,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
LAB__text__0041a4ba:
      local_8 = (undefined4 *)0x41a4c7;
      FUN__text__0056ce80();
      return;
    }
    local_14 = FUN__text__00428a40(param_2[3]);
    param_2[2] = local_14;
    if (param_2[2] == 0) {
      FUN__text__0042b2d0(&DAT_00592f84);
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff580 + 0x20,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__0041a4ba;
    }
    (**(code **)(*(int *)*local_8 + 100))(*local_8,param_2,param_2 + 1,1,param_2[2],param_2 + 3);
    local_20 = FUN__text__0056ce80();
    local_c = local_20;
    if (local_20 == -0x7fffbffb) {
      FUN__text__0041b4a0(0x80004005);
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff580 + 0x2f,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__0041a4ba;
    }
    if (local_20 == -0x7788ff42) {
      FUN__text__0041b4a0(0x887700be);
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff580 + 0x2b,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__0041a4ba;
    }
    if (local_20 != 0) {
      FUN__text__0041b4a0(local_20);
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                  DAT_005ff580 + 0x38,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__0041a4ba;
    }
    if (*param_2 == 0) {
      FUN__text__0041b200(*param_2,param_2[1],param_2[2]);
    }
    if ((*param_2 == 0) || (local_10 = param_2[2], *(int *)(local_10 + 4) == -0x73607248))
    goto LAB__text__0041a4ba;
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                DAT_005ff580 + 0x4c,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_18 = param_2[2];
    FUN__text__00428ad0(local_18);
    param_2[2] = 0;
  } while( true );
}

