
void __fastcall FUN__text__00447d00(int param_1)

{
  code *pcVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_74 [16];
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  undefined4 local_20;
  undefined1 local_1c [4];
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_74;
  for (iVar3 = 0x1c; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_18 = param_1 + 0x1a54;
  local_8 = param_1;
  _memset((void *)(param_1 + 0x1bb0),0,0x10);
  local_10 = 0;
  local_c = 1;
  do {
    if (local_c == 0) {
      local_8 = 0x448173;
      FUN__text__0056ce80();
      return;
    }
    local_20 = *(undefined4 *)(local_8 + 0x1bb0);
    switch(local_20) {
    case 0:
      iVar3 = FUN__text__00419450();
      if (iVar3 == 0) {
        local_14 = FUN__text__00448e50();
      }
      else {
        local_14 = FUN__text__00448cc0();
      }
      local_24 = local_14;
      if (local_14 == 2) {
        local_10 = 1;
        local_c = 0;
      }
      else if (local_14 == 3) {
        local_10 = 2;
        local_c = 0;
      }
      else {
        iVar3 = FUN__text__00419450();
        if (iVar3 != 0) {
          FUN__text__004498c0();
        }
        FUN__text__0044a070();
        FUN__text__0044af30();
        FUN__text__0044bb20();
        FUN__text__00448320();
        FUN__text__00448490();
        local_28 = FUN__text__00448fe0();
        if (local_28 == 1) {
          local_10 = 1;
          local_c = 0;
        }
        else if (local_28 == 2) {
          local_10 = 2;
          local_c = 0;
        }
        else if (local_28 == 3) {
          *(undefined4 *)(local_8 + 0x1bb0) = 1;
        }
      }
      goto LAB__text__00447e6e;
    case 1:
      FUN__text__00447be0();
      *(int *)(local_8 + 0x1bb0) = *(int *)(local_8 + 0x1bb0) + 1;
      break;
    case 2:
      FUN__text__004d9a80();
      FUN__text__00443bb0(0);
      FUN__text__004d9f30();
      *(int *)(local_8 + 0x1bb0) = *(int *)(local_8 + 0x1bb0) + 1;
      break;
    case 3:
      iVar3 = FUN__text__00419450();
      if (iVar3 == 0) {
        local_14 = FUN__text__00448e50();
      }
      else {
        local_14 = FUN__text__00448cc0();
      }
      local_2c = local_14;
      if (local_14 == 1) {
        local_10 = 2;
        *(undefined4 *)(local_8 + 0x1bc4) = 5;
        *(undefined4 *)(local_8 + 0x1bc8) = 1;
        *(undefined4 *)(local_8 + 0x1bb0) = 4;
      }
      else if (local_14 == 2) {
        local_10 = 1;
        *(undefined4 *)(local_8 + 0x1bc4) = 5;
        *(undefined4 *)(local_8 + 0x1bc8) = 1;
        *(undefined4 *)(local_8 + 0x1bb0) = 4;
      }
      else {
        if (local_14 != 3) {
          sVar2 = FUN__text__004d9ac0();
          if (sVar2 == 0) {
            sVar2 = FUN__text__004d9af0();
            local_30 = (int)sVar2;
            if (local_30 != 0) {
              if (local_30 == 1) {
                FUN__text__0044a590();
              }
              else {
                iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                            "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                            DAT_00606730 + 0x65,0);
                if (iVar3 != 0) {
                  pcVar1 = (code *)swi(3);
                  (*pcVar1)();
                  return;
                }
              }
            }
            *(undefined4 *)(local_8 + 0x1bb0) = 10;
          }
          FUN__text__00422360(0);
          break;
        }
        local_10 = 2;
        *(undefined4 *)(local_8 + 0x1bc4) = 8;
        *(undefined4 *)(local_8 + 0x1bc8) = 1;
        *(undefined4 *)(local_8 + 0x1bb0) = 4;
      }
LAB__text__00447e6e:
      FUN__text__004481b0();
      FUN__text__00422360(0);
      break;
    case 4:
      sVar2 = FUN__text__004d9ac0();
      if (sVar2 == 0) {
        sVar2 = FUN__text__004d9af0();
        local_34 = (int)sVar2;
        if (local_34 != 0) {
          if (local_34 == 1) {
            FUN__text__0044a590();
          }
          else {
            iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                        DAT_00606730 + 0x72,0);
            if (iVar3 != 0) {
              pcVar1 = (code *)swi(3);
              (*pcVar1)();
              return;
            }
          }
        }
        *(undefined4 *)(local_8 + 0x1bb0) = 5;
      }
      FUN__text__00422360(0);
      break;
    case 5:
      FUN__text__00447ac0();
      *(int *)(local_8 + 0x1bb0) = *(int *)(local_8 + 0x1bb0) + 1;
      break;
    case 6:
      iVar3 = FUN__text__00441630(*(undefined4 *)(local_8 + 0x1bc4),local_1c,0x200,0x180,0x3c);
      if (iVar3 != 0) {
        if (*(int *)(local_8 + 0x1bc8) == 0) {
          *(undefined4 *)(local_8 + 0x1bb0) = 3;
        }
        else {
          *(undefined4 *)(local_8 + 0x1a50) = 2;
          local_c = 0;
        }
      }
      FUN__text__004481b0();
      FUN__text__00422360(0);
      break;
    case 10:
      FUN__text__00447ac0();
      *(undefined4 *)(local_8 + 0x1bb0) = 0;
    }
  } while( true );
}

