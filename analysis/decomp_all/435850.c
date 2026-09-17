
void FUN__text__00435850(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = FUN__text__00431dd0(&DAT_005ff888);
  if (local_14 == 1) {
    local_10 = 0;
    for (local_18 = 0; local_18 != 4; local_18 = local_18 + 1) {
      local_c = FUN__text__00431d40((int)*(short *)(&DAT_005ff888 + local_18 * 2));
      iVar2 = FUN__text__0046a430(local_c);
      if (iVar2 != 0) {
        local_10 = local_c;
      }
    }
    if ((local_10 == 0) &&
       (iVar2 = FUN__text__00424f80("wk1!=0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent032.cpp",
                                    DAT_005ff894 + 0xf,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__004e29a0(1,0,(int)*(short *)(local_10 + 2));
  }
  if (local_14 == 0) {
    FUN__text__00454ab0(0xb);
  }
  else {
    if (*(int *)(local_8 + 0x2e6f4) == 0) {
      if (local_14 == 4) {
        iVar2 = FUN__text__00430ba0();
        if (iVar2 == 0) {
          FUN__text__00454ab0(5);
        }
        else {
          FUN__text__00454ab0(2);
        }
      }
      else {
        FUN__text__00454ab0(8);
      }
    }
    iVar2 = FUN__text__00430df0();
    if (iVar2 != 0) {
      FUN__text__00454ab0(0xe);
    }
  }
  local_8 = 0x4359ae;
  FUN__text__0056ce80();
  return;
}

