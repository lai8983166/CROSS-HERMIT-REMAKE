
void FUN__text__004929e0(undefined4 param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_a4 [16];
  byte local_64;
  undefined1 local_60 [44];
  undefined1 local_34 [44];
  undefined4 local_8;
  
  puVar3 = local_a4;
  for (iVar2 = 0x28; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),1);
  local_64 = *(byte *)(param_3 + 6);
  if (local_64 != 0) {
    if (local_64 < 4) {
      FUN__text__004deaa0(param_1,local_34);
      FUN__text__0046b3e0(param_1,local_34);
      FUN__text__004deaa0(param_2,local_60);
      FUN__text__0046b3e0(param_2,local_60);
      FUN__text__0048b900(0x34,param_1,param_2,local_34,local_60);
    }
    else if ((local_64 == 4) &&
            (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                         "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                         DAT_0061925c + 0x16,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x492ad6;
  FUN__text__0056ce80();
  return;
}

