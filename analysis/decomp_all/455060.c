
void __thiscall FUN__text__00455060(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 100) == 0) {
    iVar2 = FUN__text__00424f80("ScriptFile!=0",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd98 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  if ((param_2 < 0) || (*(int *)(*(int *)(local_8 + 100) + 4) <= param_2)) {
    iVar2 = FUN__text__00424f80("(0<=off)&&(off<ScriptFile->rcnt)",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd98 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = FUN__text__004214f0(*(undefined4 *)(local_8 + 100),param_2);
  if ((param_3 < 0) || (*(int *)(local_c + 4) <= param_3)) {
    iVar2 = FUN__text__00424f80("(0<=no)&&(no<fp->rcnt)",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cd98 + 9,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = FUN__text__004214f0(local_c,param_3);
  local_8 = 0x455156;
  FUN__text__0056ce80();
  return;
}

