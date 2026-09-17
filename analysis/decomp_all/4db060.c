
void FUN__text__004db060(uint param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__0042b2d0("SysBgmPlay():ST\n");
  if ((DAT_007a4a00 != 0) && (DAT_007a49fc != 0)) {
    if ((((int)param_1 < 1) || (0x22 < param_1)) &&
       (iVar2 = FUN__text__00424f80("(1<=playno)&&(playno<(sizeof(SysBgmFileTable) / sizeof(sint8*)))"
                                    ,"E:\\CrossHermit\\GAME\\SRC\\COMMON\\ComSound.cpp",
                                    DAT_006b2d80 + 7,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_8 = FUN__text__00450170((&PTR_DAT_006b2cf4)[param_1]);
    FUN__text__0041e190(local_8,param_2);
    FUN__text__0042b2d0("SysBgmPlay():ED\n");
  }
  local_8 = 0x4db117;
  FUN__text__0056ce80();
  return;
}

