
void __thiscall FUN__text__0044e4c0(int param_1,undefined4 param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_1 + 0xac;
  local_8 = param_1;
  uVar2 = FUN__text__0042ae20(param_2);
  *(undefined4 *)(local_c + 4) = uVar2;
  if (*(int *)(local_c + 4) == 0) {
    iVar3 = FUN__text__00424f80("wk->ReadAddr!=0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\PathFind.cpp",DAT_00606938 + 5
                                ,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    uVar2 = FUN__text__004214f0(*(undefined4 *)(local_c + 4),local_10);
    *(undefined4 *)(local_c + 8 + local_10 * 4) = uVar2;
  }
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    FUN__text__0044e5d0(local_10);
  }
  for (local_10 = 4; local_10 != 8; local_10 = local_10 + 1) {
    uVar2 = FUN__text__004214f0(*(undefined4 *)(local_c + 4),local_10);
    *(undefined4 *)(local_c + 8 + local_10 * 4) = uVar2;
  }
  local_8 = 0x44e5ca;
  FUN__text__0056ce80();
  return;
}

