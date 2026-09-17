
void __fastcall FUN__text__00493ed0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  uint local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = 0xf9;
  local_8 = param_1;
  do {
    if (local_18 < 0) {
      local_8 = 0x493fd2;
      FUN__text__0056ce80();
      return;
    }
    local_14 = local_8 + 0x80aec + local_18 * 0x520;
    iVar2 = FUN__text__00468d10(local_14);
    if ((iVar2 != 0) && (iVar2 = FUN__text__0046a4c0(local_14), iVar2 != 0)) {
      local_1c = (uint)*(byte *)(*(int *)(local_14 + 600) + 0x98);
      if ((9 < local_1c) &&
         (iVar2 = FUN__text__00424f80("(0<=group) && (group<10)",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlKeySelect.cpp",
                                      DAT_00619294 + 0xb,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_c = local_8 + 0x116098 + local_1c * 0x2c;
      local_10 = FUN__text__00427d60();
      *(int *)(local_10 + 8) = local_14;
      FUN__text__00427e30(local_10);
    }
    local_18 = local_18 + -1;
  } while( true );
}

