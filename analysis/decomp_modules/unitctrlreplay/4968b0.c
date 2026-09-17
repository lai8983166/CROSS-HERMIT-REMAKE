
void FUN__text__004968b0(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = FUN__text__00496450();
  if (iVar3 != 0) {
    uVar2 = FUN__text__0042ae20("ReplayData.rep");
    *(undefined4 *)(local_8 + 0x117c40) = uVar2;
    if ((*(int *)(local_8 + 0x117c40) == 0) &&
       (iVar3 = FUN__text__00424f80("ReplayWork!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlRePlay.cpp",
                                    DAT_00619f74 + 6,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    puVar4 = *(undefined4 **)(local_8 + 0x117c40);
    puVar5 = (undefined4 *)&DAT_007f4488;
    for (iVar3 = 0x23; iVar3 != 0; iVar3 = iVar3 + -1) {
      *puVar5 = *puVar4;
      puVar4 = puVar4 + 1;
      puVar5 = puVar5 + 1;
    }
    for (local_c = 0; local_c != 0x50; local_c = local_c + 1) {
      puVar4 = (undefined4 *)(*(int *)(local_8 + 0x117c40) + 0x8c + local_c * 0xb0);
      puVar5 = (undefined4 *)(&DAT_007f4518 + local_c * 0xb0);
      for (iVar3 = 0x2c; iVar3 != 0; iVar3 = iVar3 + -1) {
        *puVar5 = *puVar4;
        puVar4 = puVar4 + 1;
        puVar5 = puVar5 + 1;
      }
      (&DAT_007f45b0)[local_c * 0xb0] = 0;
    }
    *(int *)(local_8 + 0x117c44) = *(int *)(local_8 + 0x117c40) + 0x378c;
    *(undefined1 *)(local_8 + 0x2ef44) = DAT_007f4490;
  }
  local_8 = 0x4969ca;
  FUN__text__0056ce80();
  return;
}

