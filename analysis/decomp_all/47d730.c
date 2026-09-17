
void FUN__text__0047d730(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_2 == 0) {
    local_c = param_1 + 0x2f4;
  }
  else {
    local_c = param_1 + 0x3e0;
  }
  local_14 = FUN__text__004380b0(local_c,param_2);
  local_10 = local_14;
  if (local_14 == -2) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e6c + 0x23,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else if ((local_14 != -1) && (local_14 == 1)) {
    *(char *)(local_c + 0x1c) =
         (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                     (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    *(char *)(local_c + 0x1d) =
         (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                     (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  }
  local_8 = 0x47d826;
  FUN__text__0056ce80();
  return;
}

