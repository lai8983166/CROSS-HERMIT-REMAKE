
void __fastcall FUN__text__0049c850(int param_1)

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
  if (*(char *)(param_1 + 0x2f15c) != -1) {
    local_8 = param_1;
    for (local_c = 0; local_c != 4; local_c = local_c + 1) {
      FUN__text__004077c0(DAT_007a49fc);
      *(undefined2 *)(local_8 + 0x1089a6 + local_c * 0x80) = 0xc4;
    }
    iVar1 = FUN__text__004577f0();
    if ((iVar1 == 0) && ((*(byte *)(local_8 + 0x2f161) & 0x80) != 0)) {
      FUN__text__00408f90(0x1d1,0x2b9);
    }
    iVar1 = FUN__text__00456b20();
    if (iVar1 == 0) {
      if ((*(byte *)(local_8 + 0x2f161) & 0x40) != 0) {
        FUN__text__00408f90(0x1d1,0x2ce);
      }
      if ((*(byte *)(local_8 + 0x2f161) & 0x20) != 0) {
        FUN__text__00408f90(0x1d1,0x2dc);
      }
      if ((*(byte *)(local_8 + 0x2f161) & 0x10) != 0) {
        FUN__text__00408f90(0x1d1,0x2ea);
      }
    }
  }
  local_8 = 0x49c9a5;
  FUN__text__0056ce80();
  return;
}

