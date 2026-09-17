
void FUN__text__004810d0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_6c [16];
  undefined1 *local_2c;
  int local_28;
  int local_24;
  char *local_20;
  undefined1 local_1c [4];
  undefined1 local_18 [4];
  undefined2 local_14;
  undefined2 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_6c;
  for (iVar2 = 0x1a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_20 = (char *)(param_1 + 0x260);
  local_10 = (undefined2)
             ((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                   (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_14 = (undefined2)
             ((int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)
                   ) >> 4);
  FUN__text__0043d4e0();
  local_c = 0;
  do {
    if (local_c == *local_20) {
      local_8 = 0x4812b9;
      FUN__text__0056ce80();
      return;
    }
    if (*(short *)(local_20 + local_c * 2 + 2) == -1) {
      iVar2 = FUN__text__00424f80("apwk->uno[i]!=-1",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                  DAT_00618ec4 + 0xd,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    local_24 = local_8 + 0x80aec + *(short *)(local_20 + local_c * 2 + 2) * 0x520;
    iVar2 = FUN__text__00468d80(local_24);
    if (iVar2 != 0) {
      iVar2 = FUN__text__0046a120(local_24);
      if (iVar2 != 0) {
        iVar2 = FUN__text__0043d660(CONCAT22((short)((uint)*(int *)(param_1 + 600) >> 0x10),local_10
                                            ),local_14,
                                    *(undefined1 *)(*(int *)(param_1 + 600) + 0x2c),
                                    *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),local_18,
                                    local_1c);
        if (iVar2 != 0) {
          local_28 = FUN__text__00427d60();
          if (local_28 == 0) {
            iVar2 = FUN__text__00424f80("list!=0",
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                        DAT_00618ec4 + 0x1f,0);
            if (iVar2 != 0) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
          local_2c = *(undefined1 **)(local_28 + 8);
          *local_2c = 4;
          local_2c[1] = local_20[local_c * 2 + 2];
          local_2c[2] = local_20[local_c * 2 + 2];
          local_2c[3] = local_18[0];
          local_2c[4] = local_1c[0];
          FUN__text__00427e30(local_28);
        }
      }
    }
    local_c = local_c + 1;
  } while( true );
}

