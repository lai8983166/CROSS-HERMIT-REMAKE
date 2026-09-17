
void __fastcall FUN__text__004678c0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  char local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(char *)(param_1 + 0x108b3b) != -1) {
    local_c = *(char *)(param_1 + 0x108b3b);
    local_8 = param_1;
    if (local_c == '\x01') {
      if (*(char *)(param_1 + 0x108b3c) == '\0') {
        FUN__text__0043b250(1);
        FUN__text__00455160(0);
        *(undefined1 *)(local_8 + 0x108b34) = 0;
        *(undefined1 *)(local_8 + 0x108b35) = 0;
        *(undefined1 *)(local_8 + 0x108b36) = 0;
        *(undefined1 *)(local_8 + 0x108b38) = 0;
        *(undefined1 *)(local_8 + 0x108b39) = 0;
        *(undefined1 *)(local_8 + 0x108b3a) = 0;
      }
      else {
        FUN__text__0043b250(0);
        FUN__text__00455160(1);
        *(undefined1 *)(local_8 + 0x108b34) = 1;
        *(undefined1 *)(local_8 + 0x108b35) = 1;
        *(undefined1 *)(local_8 + 0x108b36) = 1;
        *(undefined1 *)(local_8 + 0x108b38) = 1;
        *(undefined1 *)(local_8 + 0x108b39) = 1;
        *(undefined1 *)(local_8 + 0x108b3a) = 1;
      }
    }
    else if (local_c == '\x02') {
      if (*(char *)(param_1 + 0x108b3c) != '\0') {
        FUN__text__0043b250(1);
        FUN__text__00455160(0);
        *(undefined1 *)(local_8 + 0x108b34) = 1;
        *(undefined1 *)(local_8 + 0x108b35) = 1;
        *(undefined1 *)(local_8 + 0x108b36) = 0;
        *(undefined1 *)(local_8 + 0x108b38) = 0;
        *(undefined1 *)(local_8 + 0x108b39) = 0;
        *(undefined1 *)(local_8 + 0x108b3a) = 0;
      }
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b44 + 0x37,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    *(undefined1 *)(local_8 + 0x108b3b) = 0xff;
    *(undefined1 *)(local_8 + 0x108b3c) = 0xff;
  }
  local_8 = 0x467a99;
  FUN__text__0056ce80();
  return;
}

