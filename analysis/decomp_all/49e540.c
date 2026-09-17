
void FUN__text__0049e540(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (DAT_007a49fc != 0) {
    if ((DAT_007a4a00 == 0) &&
       (iVar2 = FUN__text__00424f80("WinCon!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\WinMain.cpp",
                                    DAT_0061b048 + 7,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__00425de0();
    FUN__text__00416fa0(DAT_007a49fc + 0xb290);
    FUN__text__0040db90();
    FUN__text__0040dc80();
    FUN__text__00415b40();
    FUN__text__00416fa0(DAT_007a49fc + 0xb2b0);
    FUN__text__004217c0();
    FUN__text__00416ff0(DAT_007a49fc + 0xb2b0);
    iVar2 = FUN__text__004154f0();
    if (iVar2 != 0) {
      *(undefined2 *)(DAT_007a49fc + 0xb288) = 0;
      local_c = FUN__text__00415610();
      if (local_c != 0) {
        *(undefined2 *)(DAT_007a49fc + 0xb288) = 1;
      }
    }
    if (*(short *)(DAT_007a49fc + 0xb288) == 0) {
      local_8 = FUN__text__00414c30();
      if ((local_8 != 0) &&
         (iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\WinMain.cpp",
                                      DAT_0061b048 + 99,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      FUN__text__00416fa0(DAT_007a49fc + 0xb2d0);
      FUN__text__0040e330();
      FUN__text__00415dd0(0,0,0xffffffff);
      FUN__text__00417090(0,0x10);
      FUN__text__00416ff0(DAT_007a49fc + 0xb2d0);
      FUN__text__00416fa0(DAT_007a49fc + 0xb2f0);
      local_8 = FUN__text__00414de0();
      if ((local_8 != 0) &&
         (iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\WinMain.cpp",
                                      DAT_0061b048 + 0x6f,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      FUN__text__00416ff0(DAT_007a49fc + 0xb2f0);
    }
    FUN__text__00412a30();
    iVar2 = FUN__text__004154f0();
    if ((iVar2 == 0) && (*(short *)(DAT_007a49fc + 0xb288) == 0)) {
      FUN__text__004152c0(0);
    }
    FUN__text__00416ff0(DAT_007a49fc + 0xb290);
    FUN__text__00417050(DAT_007a49fc + 0xb290);
    FUN__text__00417050(DAT_007a49fc + 0xb2b0);
    FUN__text__00417050(DAT_007a49fc + 0xb2d0);
    FUN__text__00417050(DAT_007a49fc + 0xb2f0);
  }
  local_8 = 0x49e841;
  FUN__text__0056ce80();
  return;
}

