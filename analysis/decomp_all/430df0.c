
void FUN__text__00430df0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00456b20();
  if ((iVar2 != 0) &&
     (iVar2 = FUN__text__00424f80("tTask->IsNetwork()==0",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlEvent.cpp",
                                  DAT_005ff73c + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_10 = 0;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar2 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if ((iVar2 != 0) &&
       (iVar2 = FUN__text__0046a4c0(local_8 + 0x80aec + local_c * 0x520), iVar2 != 0)) {
      local_10 = local_10 + 1;
    }
  }
  local_14 = 0;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar2 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if (((iVar2 != 0) &&
        (iVar2 = FUN__text__0046a4c0(local_8 + 0x80aec + local_c * 0x520), iVar2 != 0)) &&
       (iVar2 = FUN__text__004695d0(local_8 + 0x80aec + local_c * 0x520), iVar2 != 0)) {
      local_14 = local_14 + 1;
    }
  }
  local_8 = 0x430f5b;
  FUN__text__0056ce80();
  return;
}

