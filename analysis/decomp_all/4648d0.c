
void FUN__text__004648d0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = FUN__text__00427650(300);
  if (local_10 != 0) {
    iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitAiComCtrl.cpp",
                                DAT_0060d158 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  for (local_c = 0; local_c != 300; local_c = local_c + 1) {
    FUN__text__00427890(local_c,param_1 + 0x28 + local_c * 0x10);
  }
  local_8 = 0x46496d;
  FUN__text__0056ce80();
  return;
}

