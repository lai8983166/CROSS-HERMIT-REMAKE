
void FUN__text__00430980(uint param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int *local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00456b20();
  if (((iVar2 != 0) && (iVar2 = FUN__text__004daae0((int)DAT_007f4488), iVar2 == 0)) &&
     (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                  DAT_005ff730 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (int *)(local_8 + 0xdc8ec);
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    iVar2 = FUN__text__0046a550(local_c[local_10 + 1]);
    if ((iVar2 != 0) && (*(byte *)(*(int *)(local_c[local_10 + 1] + 600) + 0x98) == param_1))
    goto LAB__text__00430b09;
  }
  local_c = (int *)(local_8 + 0xdccd8);
  local_10 = 0;
  while ((local_10 != *local_c &&
         (((iVar2 = FUN__text__0046a550(local_c[local_10 + 1]), iVar2 == 0 ||
           (*(byte *)(*(int *)(local_c[local_10 + 1] + 600) + 0x98) != param_1)) ||
          (((param_2 == 0 || (*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0x96) != '\x03')) &&
           ((param_2 == 0 || (iVar2 = FUN__text__00469220(local_c[local_10 + 1]), iVar2 != 0))))))))
        ) {
    local_10 = local_10 + 1;
  }
LAB__text__00430b09:
  local_8 = 0x430b16;
  FUN__text__0056ce80();
  return;
}

