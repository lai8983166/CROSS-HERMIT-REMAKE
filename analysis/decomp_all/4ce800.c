
void FUN__text__004ce800(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0042b2d0("_YBCSysBgmStop():ST\n");
  if ((DAT_007a4a00 != 0) && (DAT_007a49fc != 0)) {
    FUN__text__0041e500();
    FUN__text__0042b2d0("_YBCSysBgmStop():ED\n");
  }
  uStack_8 = 0x4ce866;
  FUN__text__0056ce80();
  return;
}

