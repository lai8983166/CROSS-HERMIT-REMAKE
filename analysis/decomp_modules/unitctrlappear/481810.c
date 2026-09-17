
/* WARNING: Removing unreachable block (ram,0x004818a0) */

void FUN__text__00481810(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(DAT_007a49fc + 0x19b8);
  if (local_c != 1) {
    if (local_c == 2) {
      FUN__text__00481fc0();
    }
    else if (local_c == 3) {
      FUN__text__00481bf0();
      *(undefined4 *)(local_8 + 0x2a340) = 0;
    }
    else {
      FUN__text__00481580();
    }
    local_8 = 0x4818d0;
    FUN__text__0056ce80();
    return;
  }
  iVar2 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                              DAT_00618ecc + 8,0);
  if (iVar2 == 0) {
    do {
      (*DAT_00592264)(10);
      FUN__text__0056ce80();
    } while( true );
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

