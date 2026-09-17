
void FUN__text__00409b70(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4,
                        int param_5,int param_6)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_7c [16];
  int local_3c;
  int local_38;
  int local_34;
  undefined4 local_30;
  undefined4 local_2c;
  int local_28;
  undefined4 local_24;
  undefined4 local_20;
  int local_1c;
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar3 = local_7c;
  for (iVar2 = 0x1e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = 1;
  FUN__text__00409a70();
  local_14 = FUN__text__0042ae20(param_3);
  if ((local_14 == 0) &&
     (iVar2 = FUN__text__00424f80("addr!=0",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                  DAT_005ff0f0 + 0xe,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_14 != 0) {
    local_10 = local_14;
    local_c = local_14;
    if ((param_4 < 1) || (7 < *(int *)(local_14 + 4))) {
      local_20 = FUN__text__004214f0(local_14,6);
      local_34 = FUN__text__00428a40(*(undefined4 *)(local_c + 0x20));
      *local_8 = local_34;
      if (*local_8 != 0) {
        FUN__text__0056d4d0(*local_8,local_14,*(undefined4 *)(local_c + 0x20));
        local_c = *local_8;
        iVar2 = FUN__text__004214f0(local_c,0);
        local_8[1] = iVar2;
        iVar2 = FUN__text__004214f0(local_c,1);
        local_8[2] = iVar2;
        iVar2 = FUN__text__004214f0(local_c,2);
        local_8[3] = iVar2;
        iVar2 = FUN__text__004214f0(local_c,3);
        local_8[4] = iVar2;
        iVar2 = FUN__text__004214f0(local_c,4);
        local_8[5] = iVar2;
        local_24 = FUN__text__004214f0(local_c,5);
        if (param_4 < 1) {
          local_1c = FUN__text__0041ebf0(param_1,param_2,local_24,local_20,param_6);
        }
        else {
          local_28 = FUN__text__004214f0(local_10,7);
          if ((*(int *)(local_28 + 4) <= param_4 + -1) &&
             (iVar2 = FUN__text__00424f80("(pindex-1) < pfile->rcnt",
                                          "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                          DAT_005ff0f0 + 0x2b,0), iVar2 != 0)) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
          local_30 = FUN__text__004214f0(local_28,param_4 + -1);
          if (param_5 == 0) {
            local_2c = 0;
          }
          else {
            if ((*(int *)(local_10 + 4) < 9) &&
               (iVar2 = FUN__text__00424f80(&DAT_005927d0,
                                            "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp"
                                            ,DAT_005ff0f0 + 0x3f,0), iVar2 != 0)) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
            local_2c = FUN__text__004214f0(local_10,8);
          }
          local_1c = FUN__text__0041ec40(param_1,param_2,local_24,local_20,param_6,local_30,local_2c
                                        );
        }
        if (local_1c == 0) {
          local_8[0xb] = param_6;
          local_18 = 0;
        }
        else if (*local_8 != 0) {
          local_38 = *local_8;
          FUN__text__00428ad0(local_38);
          *local_8 = 0;
        }
      }
      if (local_14 != 0) {
        local_3c = local_14;
        FUN__text__00428ad0(local_14);
      }
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_00592854,
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                  DAT_005ff0f0 + 0x14,param_3);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  local_8 = (int *)0x409e76;
  FUN__text__0056ce80();
  return;
}

