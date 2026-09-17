
void __fastcall FUN__text__0049dc20(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (int *)(param_1 + 0xdc8ec);
  local_10 = 0;
  local_14 = 0;
  local_8 = param_1;
  do {
    if (local_10 == *local_c) {
      local_8 = 0x49dd25;
      FUN__text__0056ce80();
      return;
    }
    iVar2 = FUN__text__0046a4c0(local_c[local_10 + 1]);
    if (iVar2 != 0) {
      iVar2 = FUN__text__0046a7a0(local_c[local_10 + 1]);
      if (iVar2 != 0) {
        if (0x13 < local_14) {
          iVar2 = FUN__text__00424f80("cnt < 20",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                      DAT_0061b00c + 0x24,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        local_18 = *(short *)(&DAT_0061af98 + local_14 * 4) + 0x19;
        local_1c = *(short *)(&DAT_0061af9a + local_14 * 4) + 0x19;
        FUN__text__0046df90(local_c[local_10 + 1],local_18,local_1c,0);
        local_14 = local_14 + 1;
      }
    }
    local_10 = local_10 + 1;
  } while( true );
}

