
void FUN__text__00498ea0(int param_1,undefined4 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 < 0) || (0xf9 < param_1)) {
    iVar2 = FUN__text__00424f80("(0<=unit_no)&&(unit_no<(250))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_0061a004 + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = DAT_007a49f4 + 0x80c7c + param_1 * 0x520;
  FUN__text__004809a0(local_8,param_2);
  local_8 = 0x498f2a;
  FUN__text__0056ce80();
  return;
}

