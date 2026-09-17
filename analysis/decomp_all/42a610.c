
void FUN__text__0042a610(uint param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((int)param_1 < 0) || (5 < param_1)) {
    iVar2 = FUN__text__00424f80("(0<=mode) && (mode<( sizeof(ext) / sizeof(sint8*) ))",
                                "E:\\CrossHermit\\GAME\\src\\system\\System.cpp",DAT_005ff714 + 10,0
                               );
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  uStack_8 = 0x42a66f;
  FUN__text__0056ce80();
  return;
}

