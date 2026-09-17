
void FUN__text__00454fa0(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_150 [16];
  undefined1 local_110 [260];
  int local_c;
  int local_8;
  
  puVar4 = local_150;
  for (iVar3 = 0x53; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = FUN__text__00451d10();
  FUN__text__0056d810(local_110,"data\\Tactics\\Script\\%s",(&PTR_s_t0000_bin_0060bc78)[iVar3]);
  uVar2 = FUN__text__004500b0(local_110);
  local_c = FUN__text__0042ae20(uVar2);
  if ((local_c == 0) &&
     (iVar3 = FUN__text__00424f80("addr!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                  DAT_0060cd94 + 7,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  *(int *)(local_8 + 100) = local_c;
  local_8 = 0x455057;
  FUN__text__0056ce80();
  return;
}

