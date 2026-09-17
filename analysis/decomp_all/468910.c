
void FUN__text__00468910(void)

{
  undefined2 uVar1;
  short sVar3;
  uint uVar2;
  int iVar4;
  uint uVar5;
  undefined4 *puVar6;
  undefined4 local_60 [16];
  int local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar6 = local_60;
  for (iVar4 = 0x17; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  iVar4 = FUN__text__00456b20();
  if (iVar4 == 0) {
    local_20 = (int)DAT_007f4488;
    if ((local_20 != 0x62) && (DAT_007f448c._3_1_ == '\0')) {
      FUN__text__0049a480(DAT_007f4490,DAT_007f4492,CONCAT22(DAT_007f4488 >> 0xf,DAT_007f4494),
                          (int)DAT_007f44a2);
    }
  }
  else {
    for (local_14 = 0; local_14 != 4; local_14 = local_14 + 1) {
      local_1c = (uint)(char)(&DAT_007f44f4)[local_14];
      uVar2 = local_1c;
      uVar5 = local_1c;
      if (local_1c < 4) {
        sVar3 = (short)((char)(&DAT_007f44f4)[local_14] >> 7);
        switch(local_1c) {
        case 0:
          uVar2 = CONCAT22(sVar3,DAT_007f4492);
          local_c = DAT_007f4492;
          uVar5 = CONCAT22(sVar3,DAT_007f4494);
          local_10 = DAT_007f4494;
          break;
        case 1:
          local_c = DAT_007f4496;
          uVar2 = CONCAT22(sVar3,DAT_007f4498);
          local_10 = DAT_007f4498;
          break;
        case 2:
          local_c = DAT_007f449a;
          local_10 = DAT_007f449c;
          uVar5 = CONCAT22(sVar3,DAT_007f449a);
          break;
        case 3:
          local_c = DAT_007f449e;
          local_10 = DAT_007f44a0;
          uVar2 = CONCAT22(sVar3,DAT_007f449e);
          uVar5 = CONCAT22(sVar3,DAT_007f44a0);
        }
      }
      local_18 = local_1c;
      FUN__text__0049a480(local_14,CONCAT22((short)(uVar5 >> 0x10),local_c),
                          CONCAT22((short)(uVar2 >> 0x10),local_10),(int)DAT_007f44a2);
    }
  }
  FUN__text__00437a70((int)*(short *)(*(int *)(local_8 + 0x2a304) + 4),
                      (int)*(short *)(*(int *)(local_8 + 0x2a304) + 6),
                      (int)*(short *)(*(int *)(local_8 + 0x2a304) + 4) *
                      (int)*(short *)(*(int *)(local_8 + 0x2a304) + 6));
  FUN__text__0044e850((int)*(short *)(*(int *)(local_8 + 0x2a304) + 4),
                      (int)*(short *)(*(int *)(local_8 + 0x2a304) + 6),
                      (int)*(short *)(*(int *)(local_8 + 0x2a304) + 4) *
                      (int)*(short *)(*(int *)(local_8 + 0x2a304) + 6));
  FUN__text__0046d860();
  FUN__text__0049aa60();
  uVar1 = FUN__text__0046b210();
  *(undefined2 *)(local_8 + 0x108b30) = uVar1;
  *(undefined4 *)(local_8 + 0x108b50) = 0;
  _memset((void *)(local_8 + 0x108b60),0,1000);
  _memset((void *)(local_8 + 0x2f150),0,0x14);
  *(undefined1 *)(local_8 + 0x2f15d) = 0xff;
  *(undefined1 *)(local_8 + 0x2f15c) = 0xff;
  *(undefined1 *)(local_8 + 0x2f15f) = 0xff;
  *(undefined1 *)(local_8 + 0x2f15e) = 0xff;
  *(undefined1 *)(local_8 + 0x2f160) = 0;
  FUN__text__00493ed0();
  iVar4 = FUN__text__00496450();
  if ((iVar4 != 0) && (DAT_007f4491 != '\0')) {
    DAT_007f4491 = '\0';
  }
  FUN__text__0048cd30();
  local_8 = 0x468ba7;
  FUN__text__0056ce80();
  return;
}

