
void FUN__text__0049f6c0(void)

{
  short sVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_70 [12];
  undefined4 uStack_40;
  undefined4 local_30;
  int local_2c;
  undefined4 local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_70;
  for (iVar3 = 0x1b; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = FUN__text__0042ae20("data\\WorkRoom\\WorkRoom.bin");
  if (local_c != 0) {
    FUN__text__00416790(local_c,10);
  }
  local_2c = local_c;
  FUN__text__00428ad0(local_c);
  *(undefined2 *)(local_8 + 0x30) = 0;
  FUN__text__004cd7b0("data\\adv\\bin\\",&DAT_007a4a0c);
  FUN__text__004cd810(&DAT_007a4a0c,(&PTR_s_dammy_bin_00621bbc)[DAT_007a5292]);
  local_10 = FUN__text__0042ae20(&DAT_007a4a0c);
  FUN__text__00416790(local_10,0xb);
  local_30 = local_10;
  FUN__text__00428ad0(local_10);
  if (DAT_007e11a0 == 0) {
    FUN__text__004db010((int)DAT_007a55f6);
  }
  (*API_GDI32_DLL_CreateFontA)(0xc,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x4c) = uVar2;
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x4c),9);
  FUN__text__004d6420("data/YsText/MapPos0401.ybc");
  FUN__text__004d64d0(0,9);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x4c),9);
  FUN__text__004d6420("data/YsText/words.ybc");
  FUN__text__004d64d0(0,9);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x4c),0x29);
  local_1c = DAT_007a528e * 5 + -1 + DAT_007a5290;
  *(undefined2 *)(local_8 + 0x1457c) = 0;
  local_14 = 1;
  while ((&UNK_00750a41)[local_14 * 8] != -1) {
    local_20 = (char)(&UNK_00750a41)[local_14 * 8] * 5 + -1 +
               (short)(char)(&UNK_00750a42)[local_14 * 8];
    if (local_20 <= local_1c) {
      local_24 = *(short *)(local_8 + 0x1457c);
      *(short *)(local_8 + 0x1457c) = *(short *)(local_8 + 0x1457c) + 1;
      *(short *)(local_8 + 0x13dac + local_24 * 4) = local_20;
      *(short *)(local_8 + 0x13dae + local_24 * 4) = local_14;
    }
    local_14 = local_14 + 1;
  }
  for (local_14 = 0; sVar1 = local_14, local_14 < *(short *)(local_8 + 0x1457c);
      local_14 = local_14 + 1) {
    while (local_18 = sVar1 + 1, local_18 < *(short *)(local_8 + 0x1457c)) {
      sVar1 = local_18;
      if (*(short *)(local_8 + 0x13dac + local_14 * 4) <
          *(short *)(local_8 + 0x13dac + local_18 * 4)) {
        local_28 = *(undefined4 *)(local_8 + 0x13dac + local_14 * 4);
        *(undefined4 *)(local_8 + 0x13dac + local_14 * 4) =
             *(undefined4 *)(local_8 + 0x13dac + local_18 * 4);
        *(undefined4 *)(local_8 + 0x13dac + local_18 * 4) = local_28;
      }
    }
  }
  for (local_14 = 0; local_14 < *(short *)(local_8 + 0x1457c); local_14 = local_14 + 1) {
    FUN__text__004d6150((&PTR_DAT_00750a44)[*(short *)(local_8 + 0x13dae + local_14 * 4) * 2]);
  }
  FUN__text__0049f660(local_8 + 0x50,"data/AllResult/AnmAllResult.bin",0x10);
  FUN__text__00409ef0(local_8 + 0xa4);
  FUN__text__004077c0(DAT_007a49fc);
  uStack_40 = 0x49fa95;
  FUN__text__0056ce80();
  return;
}

