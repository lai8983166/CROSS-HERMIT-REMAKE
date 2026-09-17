
void __fastcall FUN__text__00494690(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((((*(char *)(param_1 + 0x108b3a) != '\0') && (*(short *)(param_1 + 0x108b32) != 0)) &&
       (*(char *)(param_1 + 0x108b34) != '\0')) &&
      ((*(char *)(param_1 + 0x108b36) != '\0' && (*(char *)(param_1 + 0x108b38) != '\0')))) &&
     (local_8 = param_1, iVar1 = FUN__text__004577f0(), iVar1 == 0)) {
    local_c = 0;
    while (((local_c != 10 &&
            (iVar1 = FUN__text__004128f0((&DAT_00619280)[local_c * 2],1), iVar1 == 0)) &&
           (iVar1 = FUN__text__004128f0((&DAT_00619281)[local_c * 2],1), iVar1 == 0))) {
      local_c = local_c + 1;
    }
  }
  local_8 = 0x4947a2;
  FUN__text__0056ce80();
  return;
}

