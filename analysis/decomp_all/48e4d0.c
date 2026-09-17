
void __thiscall FUN__text__0048e4d0(undefined4 param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; local_8 = param_1, iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  while( true ) {
    local_c = FUN__text__0048e0a0(param_2,param_3);
    if (local_c == 0) {
      local_8 = 0x48e5c8;
      FUN__text__0056ce80();
      return;
    }
    if ((*(int *)(local_c + 8) == 0) &&
       (iVar2 = FUN__text__00424f80("list->data",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618fa8 + 0xd,0), iVar2 != 0)) break;
    local_14 = *(undefined4 *)(local_c + 8);
    local_1c = param_3;
    local_10 = local_14;
    if (param_3 == 0xc) {
      local_18 = FUN__text__0048ebf0(param_2,local_14);
    }
    if (local_18 == 0) {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                  DAT_00618fa8 + 0x1e,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    else {
      FUN__text__00427cd0(local_c);
    }
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

