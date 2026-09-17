
void FUN__text__004548e0(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__004500b0("data\\adv\\bin\\Gybc_00.bin");
  local_c = FUN__text__0042ae20(uVar2);
  if (local_c == 0) {
    iVar3 = FUN__text__00424f80("addr!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd88 + 3,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  FUN__text__00416790(local_c,0x14);
  local_10 = local_c;
  FUN__text__00428ad0(local_c);
  local_8 = 0x454973;
  FUN__text__0056ce80();
  return;
}

