
void __fastcall FUN__text__004498c0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  uint local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_20 = param_1 + 0x1a54;
  local_10 = 0;
  local_8 = param_1;
  iVar2 = FUN__text__00419450();
  if (iVar2 != 0) {
    local_1c = *(uint *)(DAT_007a49fc + 0x199c) & 1;
    local_c = FUN__text__0044c710(&DAT_00605d78,8);
    if (local_c == -1) {
      local_14 = FUN__text__00428380();
      if (6 < local_14) {
        local_14 = 7;
      }
      local_c = FUN__text__0044c710(&DAT_00605db8,local_14);
      if (local_c == -1) {
        local_14 = FUN__text__00428380();
        if (6 < local_14) {
          local_14 = 7;
        }
        local_c = FUN__text__0044c710(&DAT_00605e08,local_14);
        if (local_c != -1) {
          if (local_1c != 0) {
            local_34 = local_c;
            if ((local_c < 0) || (9 < local_c)) {
              iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                          "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                          DAT_00606754 + 0x85,0);
              if (iVar2 != 0) {
                pcVar1 = (code *)swi(3);
                (*pcVar1)();
                return;
              }
            }
            else {
              FUN__text__004282b0(CONCAT22(extraout_var_00,(undefined2)local_c));
              *(undefined1 *)(local_20 + 0x37) = 1;
              FUN__text__004db2b0(5);
            }
          }
          local_10 = 1;
        }
      }
      else {
        if (local_1c != 0) {
          local_30 = local_c;
          if ((local_c < 0) || (9 < local_c)) {
            iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                        DAT_00606754 + 100,0);
            if (iVar2 != 0) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
          else {
            FUN__text__004282b0(CONCAT22(extraout_var,(undefined2)local_c));
            *(undefined1 *)(local_20 + 0x37) = 0;
            FUN__text__004db2b0(5);
          }
        }
        local_10 = 1;
      }
    }
    else {
      if (local_1c != 0) {
        local_2c = local_c;
        switch(local_c) {
        case 0:
          FUN__text__00428720();
          FUN__text__004db2b0(5);
          break;
        case 1:
          FUN__text__00428520();
          FUN__text__004db2b0(5);
          break;
        case 2:
          FUN__text__004285f0();
          FUN__text__004db2b0(5);
          break;
        case 3:
          FUN__text__00428760();
          FUN__text__004db2b0(5);
          break;
        case 4:
          FUN__text__00428720();
          FUN__text__004db2b0(5);
          break;
        case 5:
          FUN__text__00428520();
          FUN__text__004db2b0(5);
          break;
        case 6:
          FUN__text__004285f0();
          FUN__text__004db2b0(5);
          break;
        case 7:
          FUN__text__00428760();
          FUN__text__004db2b0(5);
        }
        if (local_c < 4) {
          *(undefined1 *)(local_20 + 0x37) = 0;
        }
        else if (local_c < 8) {
          *(undefined1 *)(local_20 + 0x37) = 1;
        }
        else {
          iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_00606754 + 0x42,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
      }
      if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
        local_c = -1;
      }
      FUN__text__00449d00(local_c);
      local_10 = 1;
    }
  }
  local_28 = (int)*(short *)(local_20 + 0x34);
  local_24 = FUN__text__004494b0();
  if (local_24 != *(short *)(local_20 + 0x34)) {
    *(undefined2 *)(local_20 + 0x34) = (undefined2)local_24;
    FUN__text__00449fd0();
    FUN__text__0044ba50(local_28,(int)*(short *)(local_20 + 0x34));
    iVar2 = FUN__text__00419450();
    if (((iVar2 != 0) && (local_18 = FUN__text__00441fe0(), local_18 != 0)) &&
       (iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp"
                                    ,DAT_00606754 + 0xa0,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x449cd7;
  FUN__text__0056ce80();
  return;
}

