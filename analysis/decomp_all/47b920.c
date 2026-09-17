
void FUN__text__0047b920(undefined4 param_1,short *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  local_c = FUN__text__0047a8e0(param_1);
  if (0xf9 < *param_2) {
    iVar2 = FUN__text__00424f80("*unit_no < (250)",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e44 + 10,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_10 = local_8 + 0x80aec + *param_2 * 0x520;
  iVar2 = FUN__text__00468d10(local_10);
  if (iVar2 != 0) {
    iVar2 = FUN__text__00469480(local_10);
    if (iVar2 != 0) {
      iVar2 = FUN__text__0047c580(param_1,local_10);
      if (iVar2 != 0) {
        FUN__text__00475270(param_1,6);
        FUN__text__00437d90(param_1,0);
        local_14 = 1;
      }
    }
  }
  FUN__text__00492e60(param_2);
  local_8 = 0x47ba17;
  FUN__text__0056ce80();
  return;
}

