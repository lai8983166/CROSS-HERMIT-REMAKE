
void FUN__text__004964f0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_64 [16];
  undefined4 *local_24;
  undefined4 *local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  undefined4 *local_c;
  undefined4 local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00496410();
  if (iVar2 != 0) {
    local_20 = (undefined4 *)FUN__text__00428a40(0x37a8);
    local_c = local_20;
    if ((local_20 == (undefined4 *)0x0) &&
       (iVar2 = FUN__text__00424f80("repw!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlRePlay.cpp",
                                    DAT_00619f68 + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    _memset(local_c,0,0x37a8);
    puVar3 = (undefined4 *)&DAT_007f4488;
    puVar4 = local_c;
    for (iVar2 = 0x23; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
    for (local_14 = 0; local_14 != 0x50; local_14 = local_14 + 1) {
      puVar3 = (undefined4 *)(&DAT_007f4518 + local_14 * 0xb0);
      puVar4 = local_c + local_14 * 0x2c + 0x23;
      for (iVar2 = 0x2c; iVar2 != 0; iVar2 = iVar2 + -1) {
        *puVar4 = *puVar3;
        puVar3 = puVar3 + 1;
        puVar4 = puVar4 + 1;
      }
    }
    local_1c = 0x378c;
    local_10 = FUN__text__0056e7c0("ReplayData.rep",&DAT_00595078);
    if ((local_10 == 0) &&
       (iVar2 = FUN__text__00424f80("fp != 0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlRePlay.cpp",
                                    DAT_00619f68 + 0x13,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_18 = FUN__text__00570d70(local_c,1,local_1c,local_10);
    if ((local_18 != local_1c) &&
       (iVar2 = FUN__text__00424f80("ret==size",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlRePlay.cpp",
                                    DAT_00619f68 + 0x15,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__0056e4a0(local_10);
    local_24 = local_c;
    FUN__text__00428ad0(local_c);
  }
  local_8 = 0x49667d;
  FUN__text__0056ce80();
  return;
}

