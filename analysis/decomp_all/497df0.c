
void FUN__text__00497df0(int param_1,undefined4 param_2)

{
  int iVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if ((param_1 < 0) || (0xf9 < param_1)) {
    iVar3 = FUN__text__00424f80("(0<=unitno) && (unitno<(250))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fcc + 3,0);
    if (iVar3 != 0) {
      pcVar2 = (code *)swi(3);
      (*pcVar2)();
      return;
    }
  }
  iVar3 = *(int *)(DAT_007a49f4 + 0x80f68 + param_1 * 0x520);
  iVar1 = *(int *)(DAT_007a49f4 + 0x80f6c + param_1 * 0x520);
  local_8 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5;
  local_c = (int)((iVar1 >> 0x10) + (iVar1 >> 0x1f & 0xfU)) >> 4;
  FUN__text__00498010(local_8,local_c,param_2);
  local_8 = 0x497eb2;
  FUN__text__0056ce80();
  return;
}

