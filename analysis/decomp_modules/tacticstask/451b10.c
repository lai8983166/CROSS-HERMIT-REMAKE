
void FUN__text__00451b10(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__004500b0("data\\Tactics\\common.bin");
  local_10 = FUN__text__0042ae20(uVar2);
  if (local_10 == 0) {
    iVar3 = FUN__text__00424f80("addr != 0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd74 + 7,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__00416790(local_10,0x5a);
  if (local_c != 0) {
    iVar3 = FUN__text__00424f80("ret == 0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd74 + 9,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_14 = local_10;
  FUN__text__00428ad0(local_10);
  FUN__text__00458ff0();
  FUN__text__00459080();
  local_8 = 0x451be2;
  FUN__text__0056ce80();
  return;
}

