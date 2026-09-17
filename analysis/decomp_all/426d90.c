
void FUN__text__00426d90(char *param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  char *local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_3 < 2) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                DAT_005ff698 + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    (*API_KERNEL32_DLL_lstrlenA)(param_2);
    local_1c = FUN__text__0056ce80();
    if (local_1c + 1 < param_3) {
      local_10 = (char *)(param_2 + local_1c);
      local_c = param_1;
      local_14 = param_3;
      local_20 = param_3 - local_1c;
      local_18 = local_1c;
      while (*local_c != '\0') {
        iVar2 = FUN__text__00429820(CONCAT31(*local_c >> 7,*local_c));
        if (iVar2 == 0) {
          if (local_20 + -2 < 0) goto LAB__text__00426ef7;
          *local_10 = *local_c;
          local_10 = local_10 + 1;
          local_c = local_c + 1;
          *local_10 = '\0';
          local_20 = local_20 + -1;
        }
        else {
          if (local_20 + -3 < 0) goto LAB__text__00426ef7;
          *local_10 = *local_c;
          local_10[1] = local_c[1];
          local_10 = local_10 + 2;
          local_c = local_c + 2;
          *local_10 = '\0';
          local_20 = local_20 + -2;
        }
      }
      *local_10 = '\0';
    }
  }
LAB__text__00426ef7:
  local_8 = 0x426f04;
  FUN__text__0056ce80();
  return;
}

