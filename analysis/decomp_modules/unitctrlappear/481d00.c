
void FUN__text__00481d00(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  undefined1 *local_24;
  int local_20;
  undefined1 local_1c [4];
  undefined1 local_18 [4];
  undefined2 local_14;
  undefined2 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = (undefined2)
             ((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                   (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_14 = (undefined2)
             ((int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)
                   ) >> 4);
  FUN__text__0043d4e0();
  local_c = 0;
  do {
    if (local_c == *(int *)(local_8 + 0x108b50)) {
      local_8 = 0x481ee1;
      FUN__text__0056ce80();
      return;
    }
    if (*(char *)(*(int *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 600) + 0xa4) !=
        *(char *)(local_8 + 0x2ef44)) {
      iVar2 = FUN__text__00424f80("select_uw[i]->data->player==PlayerNo",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                  DAT_00618ed8 + 0xb,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    iVar2 = FUN__text__0046a7a0(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4));
    if (iVar2 != 0) {
      iVar2 = FUN__text__0043d660(CONCAT22((short)((uint)*(int *)(param_1 + 600) >> 0x10),local_10),
                                  local_14,*(undefined1 *)(*(int *)(param_1 + 600) + 0x2c),
                                  *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),local_18,local_1c)
      ;
      if (iVar2 != 0) {
        local_20 = FUN__text__00427d60();
        if (local_20 == 0) {
          iVar2 = FUN__text__00424f80("list!=0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                      DAT_00618ed8 + 0x1a,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        local_24 = *(undefined1 **)(local_20 + 8);
        *local_24 = 4;
        local_24[1] = *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 2);
        local_24[2] = *(undefined1 *)(*(int *)(local_8 + 0x108b60 + local_c * 4) + 2);
        local_24[3] = local_18[0];
        local_24[4] = local_1c[0];
        FUN__text__00427e30(local_20);
      }
    }
    local_c = local_c + 1;
  } while( true );
}

