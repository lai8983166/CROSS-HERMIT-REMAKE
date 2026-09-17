
/* WARNING: Removing unreachable block (ram,0x00448f9c) */

void FUN__text__00448e50(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_70 [16];
  int local_30;
  int local_2c;
  int local_28;
  undefined4 local_24;
  undefined1 local_20 [8];
  undefined4 local_18;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = 0;
  local_28 = FUN__text__0041a120(0);
  if (local_28 == -1) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                DAT_00606740 + 0x29,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else if (local_28 == 1) {
    do {
      while( true ) {
        while (local_2c = FUN__text__0041a1e0(local_20), local_c = local_2c, local_2c == -1) {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_00606740 + 0x23,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        if (local_2c != 0) break;
        local_30 = FUN__text__00443780(local_20);
        local_c = local_30;
        if (local_30 == -2) {
          local_10 = 3;
        }
        else if (local_30 == -1) {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_00606740 + 0x16,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        else if (local_30 == 1) {
          local_10 = 2;
        }
        local_24 = local_18;
        FUN__text__00428ad0(local_18);
      }
    } while (local_2c != 1);
    local_2c = 1;
    local_c = 1;
  }
  local_8 = 0x448fdb;
  FUN__text__0056ce80();
  return;
}

