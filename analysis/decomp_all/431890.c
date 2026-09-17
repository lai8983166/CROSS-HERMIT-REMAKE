
void FUN__text__00431890(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00496450();
  for (local_c = 0;
      (local_c != 4 &&
      (((&DAT_007f44d4)[local_c] == '\0' || (*(short *)(param_1 + 0x1e + local_c * 0x32) != 0))));
      local_c = local_c + 1) {
  }
  local_8 = 0x431905;
  FUN__text__0056ce80();
  return;
}

