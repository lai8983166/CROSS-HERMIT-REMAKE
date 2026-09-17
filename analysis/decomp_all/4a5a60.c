
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004a5a60(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  DAT_007a4e62 = 1;
  local_10 = FUN__text__0042ae20("data\\menu\\HanData.bin");
  if (local_10 != 0) {
    FUN__text__00416790(local_10,0xc);
  }
  local_14 = local_10;
  FUN__text__00428ad0(local_10);
  (*API_GDI32_DLL_CreateFontA)(0xf,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  uVar1 = FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x794c) = uVar1;
  FUN__text__004d0860();
  FUN__text__004a8140(local_8 + 0x34,"data\\menu\\AnmHan.bin",0x10);
  for (local_c = 0; local_c < 5; local_c = local_c + 1) {
    FUN__text__00409ef0(local_8 + 0x88 + local_c * 0x58);
    *(undefined2 *)(local_8 + 0x2c0 + local_c * 2) = 0xffff;
  }
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x794c),10);
  FUN__text__004d6420("data/YsText/TacticsExp.ybc");
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x794c),10);
  FUN__text__004d6420("data/YsText/LectureExp.ybc");
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x794c),5);
  *(undefined2 *)(local_8 + 0x76c8) = 0;
  *(undefined2 *)(local_8 + 0x76c6) = 2;
  DAT_007d5982 = 0;
  DAT_007d5984 = 0;
  DAT_007d5985 = 0;
  DAT_007d5986 = 0;
  _DAT_007d5988 = 0xffff;
  DAT_007d598a = 0;
  DAT_007d598b = 0;
  DAT_007d598c = 0;
  DAT_007d598d = 0;
  DAT_007d57d9 = 0xff;
  DAT_007a4e60 = 0;
  *(undefined2 *)(local_8 + 0x128e) = 0xffff;
  *(undefined2 *)(local_8 + 0x1290) = 0xffff;
  *(undefined2 *)(local_8 + 0x1292) = 0xffff;
  DAT_007d57c6 = 0;
  DAT_007d57cc = 0;
  DAT_007d57ce = 0;
  FUN__text__004a9ab0();
  DAT_007a55fa = 0;
  FUN__text__004a17b0();
  FUN__text__004a2ba0();
  local_8 = 0x4a5cd1;
  FUN__text__0056ce80();
  return;
}

