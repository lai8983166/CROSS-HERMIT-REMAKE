
void FUN__text__00440c10(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  short local_24;
  int local_20;
  int local_1c;
  short local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = FUN__text__00403910(&local_10);
  if (local_14 != 0) {
    iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                DAT_005ffa30 + 9,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_24 = *(short *)(local_8 + 0x26544) << 1;
  for (local_18 = 0; local_18 != *(short *)(local_8 + 0x26546); local_18 = local_18 + 1) {
    local_1c = *(int *)(local_8 + 0x2658c) + (int)local_18 * (int)local_24;
    local_20 = local_c + local_18 * local_10;
    FUN__text__0056d4d0(local_20,local_1c,(int)local_24);
  }
  local_14 = FUN__text__00403990();
  if (local_14 != 0) {
    iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                DAT_005ffa30 + 0x12,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x440d2d;
  FUN__text__0056ce80();
  return;
}

