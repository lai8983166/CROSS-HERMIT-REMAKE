
void FUN__text__004bd870(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined **ppuVar5;
  undefined4 local_58 [16];
  undefined4 local_18;
  short local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ppuVar5 = &PTR_s_data_Sound_plw_ARSND_SE_LUP00_wa_0061c5e4;
  uVar2 = FUN__text__00450110(&DAT_005953ac);
  local_c = FUN__text__0040c780(1,uVar2,ppuVar5);
  if ((local_c != 0) &&
     (iVar3 = FUN__text__00424f80("ret == 0",
                                  "e:\\crosshermit\\game\\src\\yoshimaru\\allresult\\allresult_init.cpp"
                                  ,DAT_0061c5fc + 0x2e,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  FUN__text__004d1c60();
  DAT_007e1180 = 0xffff;
  DAT_007e1182 = 0;
  DAT_007e1184 = 0;
  DAT_007e1188 = 0;
  DAT_007e118e = 0;
  DAT_007e118c = 0;
  DAT_007e1190 = 0;
  DAT_007e1194 = 0;
  DAT_007e1196 = 0;
  DAT_007e1198 = 0;
  DAT_007e119c = 0;
  *(undefined2 *)(local_8 + 0x142c) = 0;
  *(undefined2 *)(local_8 + 0x142e) = 1;
  local_10 = FUN__text__0042ae20("data/AllResult/AllResult.bin");
  FUN__text__00416790(local_10,0xf);
  local_18 = local_10;
  FUN__text__00428ad0(local_10);
  FUN__text__004d0860();
  FUN__text__004bffc0();
  *(undefined4 *)(local_8 + 0x34) = 0;
  if (DAT_007f4491 == '\0') {
    FUN__text__004c00c0();
  }
  else if (DAT_007f4505 != '\0') {
    FUN__text__004c0350();
  }
  DAT_007a511c = DAT_007a511c + *(int *)(local_8 + 0x34);
  DAT_007a511c = FUN__text__004d1ba0(DAT_007a511c,0,999999999);
  FUN__text__004bd7e0(local_8 + 0x1430,"data/AllResult/AnmAllResult.bin",0x11);
  for (local_14 = 0; local_14 < 0xa0; local_14 = local_14 + 1) {
    FUN__text__00409ef0(local_8 + 0x1484 + local_14 * 0x58);
  }
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__00409ff0(local_8 + 0x1484,0,1,0);
  local_8 = 0x4bdab4;
  FUN__text__0056ce80();
  return;
}

