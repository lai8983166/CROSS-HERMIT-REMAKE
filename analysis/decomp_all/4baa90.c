
void FUN__text__004baa90(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  ushort local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0042ae20("data/TacticsResult/TacticsResult.bin");
  FUN__text__00416790(local_c,0xe);
  local_18 = local_c;
  FUN__text__00428ad0(local_c);
  local_10 = local_8 + 0x34;
  for (local_14 = 0; local_14 < 0x198; local_14 = local_14 + 1) {
    *(undefined1 *)(local_10 + (short)local_14) = 0;
  }
  if ((DAT_007f4491 == '\x01') && (DAT_007f4505 == '\0')) {
    *(undefined2 *)(local_8 + 0x32) = 1;
  }
  else {
    FUN__text__004bbcc0();
  }
  local_8 = 0x4bab59;
  FUN__text__0056ce80();
  return;
}

