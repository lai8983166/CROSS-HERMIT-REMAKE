
void FUN__text__004d7830(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__00450230(&DAT_005953ac);
  (*API_KERNEL32_DLL_CreateDirectoryA)(local_c,0);
  FUN__text__0056ce80();
  FUN__text__004d6710();
  DAT_007e11a0 = 1;
  local_10 = FUN__text__0042ae20("data/SLProg/SLProg.bin");
  FUN__text__00416790(local_10,0x12);
  local_18 = local_10;
  FUN__text__00428ad0(local_10);
  (*API_GDI32_DLL_CreateFontA)(0xb,0,0,0,400,0,0,0,1,5,0,0,1,&DAT_00592c9c);
  uVar1 = FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x19ab0) = uVar1;
  (*API_GDI32_DLL_CreateFontA)(0xf,0,0,0,400,0,0,0,1,5,0,0,1,&DAT_00592c9c);
  uVar1 = FUN__text__0056ce80();
  *(undefined4 *)(local_8 + 0x19ab4) = uVar1;
  *(undefined2 *)(local_8 + 0x2c724) = 0xffff;
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x19ab4),5);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x19ab0),0x50);
  FUN__text__004d6090(*(undefined4 *)(local_8 + 0x19ab0),1);
  for (local_14 = 0; local_14 != 2; local_14 = local_14 + 1) {
    FUN__text__004077c0(DAT_007a49fc);
    FUN__text__00409480(*(undefined4 *)(local_8 + 0x19ab0));
  }
  local_8 = 0x4d79ff;
  FUN__text__0056ce80();
  return;
}

