
void __fastcall FUN__text__00466b40(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  undefined4 local_28;
  int local_24;
  undefined4 local_20;
  char *local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__005900bb;
  local_10 = ExceptionList;
  puVar3 = local_68;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = 0;
  do {
    local_14 = param_1;
    if (local_18 == 0x200) {
      ExceptionList = &local_10;
      iVar2 = FUN__text__00424f80(&DAT_0059c404,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b2c + 0xd,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
LAB__text__00466c5b:
      ExceptionList = local_10;
      local_8 = 0x466c72;
      FUN__text__0056ce80();
      return;
    }
    local_1c = (char *)(param_1 + 0x2a6f0 + local_18 * 8);
    if (*local_1c == '\0') {
      ExceptionList = &local_10;
      *local_1c = '\x01';
      local_24 = FUN__text__00428a40(0x54);
      local_8 = 0;
      if (local_24 == 0) {
        local_28 = 0;
      }
      else {
        local_28 = FUN__text__00464c60();
      }
      local_20 = local_28;
      local_8 = 0xffffffff;
      *(undefined4 *)(local_1c + 4) = local_28;
      if ((*(int *)(local_1c + 4) == 0) &&
         (iVar2 = FUN__text__00424f80("tbl->anim != 0",
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                      DAT_00618b2c + 9,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__00466c5b;
    }
    local_18 = local_18 + 1;
  } while( true );
}

