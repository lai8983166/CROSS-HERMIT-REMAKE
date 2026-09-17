
void __fastcall FUN__text__0043c9c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x26598) == '\0') {
    if (*(int *)(DAT_007a49fc + 0x19b8) == 0) {
      *(undefined4 *)(param_1 + 0x265d8) = 0;
    }
    else {
      if ((((0x1d < *(int *)(DAT_007a49fc + 0x1970)) && (*(int *)(DAT_007a49fc + 0x1970) < 600)) &&
          (0x1d < *(int *)(DAT_007a49fc + 0x19c0))) && (*(int *)(DAT_007a49fc + 0x19c0) < 600)) {
        *(undefined4 *)(param_1 + 0x265d8) = 1;
      }
      local_8 = param_1;
      if ((*(int *)(param_1 + 0x265d8) == 1) && (*(int *)(DAT_007a49fc + 0x19b8) == 3)) {
        FUN__text__0043cab0();
      }
      else {
        FUN__text__0043cc50();
      }
    }
  }
  else {
    *(undefined4 *)(param_1 + 0x265d8) = 0;
  }
  local_8 = 0x43caa2;
  FUN__text__0056ce80();
  return;
}

