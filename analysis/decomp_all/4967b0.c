
void FUN__text__004967b0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_70 [16];
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00496410();
  if (iVar2 != 0) {
    local_30 = 0x7fffffff;
    local_2c = *(undefined4 *)(local_8 + 0x2e70c);
    local_28 = *(undefined4 *)(local_8 + 0x2e710);
    local_14 = 0x1c;
    local_c = FUN__text__0056e7c0("ReplayData.rep",&PTR_DAT_0059e784);
    if ((local_c == 0) &&
       (iVar2 = FUN__text__00424f80("fp != 0",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlRePlay.cpp",
                                    DAT_00619f70 + 0x11,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_10 = FUN__text__00570d70(&local_30,1,local_14,local_c);
    if ((local_10 != local_14) &&
       (iVar2 = FUN__text__00424f80("ret == size",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlRePlay.cpp",
                                    DAT_00619f70 + 0x13,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__0056e4a0(local_c);
  }
  local_8 = 0x4968a5;
  FUN__text__0056ce80();
  return;
}

