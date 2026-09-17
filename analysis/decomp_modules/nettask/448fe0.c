
void __fastcall FUN__text__00448fe0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = param_1 + 0x1a54;
  local_10 = 0;
  local_8 = param_1;
  local_c = FUN__text__0044c710(&DAT_00605d18,6);
  if ((local_c != -1) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
    local_24 = local_c;
    switch(local_c) {
    case 0:
      iVar2 = FUN__text__00419450();
      if (iVar2 == 0) {
        local_c = -1;
      }
      else {
        iVar2 = FUN__text__0041af20();
        if (((iVar2 != 0) && (iVar2 = FUN__text__0044adb0(), iVar2 != 0)) &&
           (iVar2 = FUN__text__004192e0(0), iVar2 == 0)) {
          local_14 = FUN__text__00441f40();
          if (local_14 != 0) {
            FUN__text__004192e0(1);
          }
          local_10 = 1;
          FUN__text__004db2b0(5);
        }
      }
      break;
    case 1:
      iVar2 = FUN__text__00441b90();
      if (iVar2 == 0) {
        local_10 = 2;
        FUN__text__004db2b0(5);
      }
      break;
    case 2:
      iVar2 = FUN__text__00419450();
      if (iVar2 == 0) {
        iVar2 = FUN__text__00441b90();
        if (iVar2 == 0) {
          iVar2 = FUN__text__0044adb0();
          if ((iVar2 != 0) && (local_1c = FUN__text__0041ade0(), local_1c != 0)) {
            iVar2 = FUN__text__00441de0();
            if (iVar2 != 0) {
              local_20 = FUN__text__0041ade0();
              if ((local_20 == 0) &&
                 (iVar2 = FUN__text__00424f80("jw != 0",
                                              "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                              DAT_00606744 + 0x4d,0), iVar2 != 0)) {
                pcVar1 = (code *)swi(3);
                (*pcVar1)();
                return;
              }
              if ((*(char *)(local_20 + 1) != '\0') &&
                 (iVar2 = FUN__text__00424f80("jw->Ready == 0",
                                              "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                              DAT_00606744 + 0x4e,0), iVar2 != 0)) {
                pcVar1 = (code *)swi(3);
                (*pcVar1)();
                return;
              }
            }
            FUN__text__00442f40();
          }
        }
        else {
          FUN__text__004427d0();
        }
        FUN__text__004db2b0(5);
      }
      else {
        local_c = -1;
      }
      break;
    case 3:
      FUN__text__004db2b0(5);
      break;
    case 4:
      iVar2 = FUN__text__00441b90();
      if (iVar2 == 0) {
        FUN__text__004db2b0(5);
        FUN__text__0044a960();
        FUN__text__0044aaf0();
      }
      break;
    case 5:
      iVar2 = FUN__text__00441b90();
      if (iVar2 == 0) {
        FUN__text__004db2b0(5);
        local_10 = 3;
      }
    }
  }
  if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
    local_c = -1;
  }
  if ((local_c == 0) && (iVar2 = FUN__text__00419450(), iVar2 == 0)) {
    local_c = -1;
  }
  FUN__text__004492d0(local_c);
  local_8 = 0x4492ab;
  FUN__text__0056ce80();
  return;
}

