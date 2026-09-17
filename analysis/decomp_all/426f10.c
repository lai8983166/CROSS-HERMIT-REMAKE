
void FUN__text__00426f10(char *param_1,char *param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  char *local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_3 == 0) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                DAT_005ff69c + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    local_c = param_1;
    local_14 = param_3;
    local_10 = param_2;
    while (*local_c != '\0') {
      iVar2 = FUN__text__00429820(CONCAT31(*local_c >> 7,*local_c));
      if (iVar2 == 0) {
        if (local_14 + -2 < 0) goto LAB__text__0042703f;
        *local_10 = *local_c;
        local_10 = local_10 + 1;
        local_c = local_c + 1;
        *local_10 = '\0';
        local_14 = local_14 + -1;
      }
      else {
        if (local_14 + -3 < 0) goto LAB__text__0042703f;
        *local_10 = *local_c;
        local_10[1] = local_c[1];
        local_10 = local_10 + 2;
        local_c = local_c + 2;
        *local_10 = '\0';
        local_14 = local_14 + -2;
      }
    }
    *local_10 = '\0';
  }
LAB__text__0042703f:
  local_8 = 0x42704c;
  FUN__text__0056ce80();
  return;
}

