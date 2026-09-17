
void FUN__text__00451bf0(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_15c [16];
  int local_11c;
  undefined1 local_118 [260];
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_15c;
  for (iVar3 = 0x56; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_14 = FUN__text__00451d10();
  FUN__text__0056d810(local_118,"data\\Tactics\\TactStart\\%s",
                      (&PTR_s_TactStart0_bin_0060c2b8)[local_14]);
  uVar2 = FUN__text__004500b0(local_118);
  local_10 = FUN__text__0042ae20(uVar2);
  if (local_10 == 0) {
    iVar3 = FUN__text__00424f80("addr != 0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd78 + 0xb,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__00416790(local_10,0x5b);
  if (local_c != 0) {
    iVar3 = FUN__text__00424f80("ret == 0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd78 + 0xd,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_11c = local_10;
  FUN__text__00428ad0(local_10);
  FUN__text__004548e0();
  FUN__text__00454fa0();
  local_8 = 0x451cfd;
  FUN__text__0056ce80();
  return;
}

