
void FUN__text__00452040(void)

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
  iVar1 = FUN__text__00452cf0();
  if (iVar1 == 0) {
    iVar1 = FUN__text__00456b20();
    if ((iVar1 == 0) && ('\x14' < DAT_007f448c._1_1_)) {
      DAT_007f448c._1_1_ = '\x14';
    }
    for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
      FUN__text__00452130(&DAT_007f4518 + local_c * 0xb0);
      (&DAT_007f45b7)[local_c * 0xb0] = 0;
      (&DAT_007f45b8)[local_c * 0xb0] = 0;
      (&DAT_007f45b3)[local_c * 0xb0] = 0;
      (&DAT_007f45b4)[local_c * 0xb0] = 0;
    }
  }
  FUN__text__00496490();
  local_8 = 0x45211e;
  FUN__text__0056ce80();
  return;
}

