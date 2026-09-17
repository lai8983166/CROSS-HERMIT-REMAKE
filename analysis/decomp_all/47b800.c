
void FUN__text__0047b800(undefined4 param_1,short *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*param_2 != -1) {
    if ((0xf9 < *param_2) &&
       (iVar2 = FUN__text__00424f80("*unit_no < (250)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e40 + 6,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = FUN__text__0047a8e0(param_1);
    local_10 = local_8 + 0x80aec + *param_2 * 0x520;
    iVar2 = FUN__text__00469ad0(local_10);
    if ((((iVar2 != 0) && (*(char *)(local_c + 0x1c) == '\0')) ||
        (iVar2 = FUN__text__00468d10(local_10), iVar2 == 0)) ||
       (((iVar2 = FUN__text__0046ae20(param_1,local_10), iVar2 == 0 ||
         (iVar2 = FUN__text__00469480(local_10), iVar2 == 0)) ||
        (iVar2 = FUN__text__004690a0(local_10), iVar2 != 0)))) {
      FUN__text__00492e60(param_2);
    }
  }
  local_8 = 0x47b90c;
  FUN__text__0056ce80();
  return;
}

