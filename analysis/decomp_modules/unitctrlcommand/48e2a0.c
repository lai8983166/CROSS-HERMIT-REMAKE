
void FUN__text__0048e2a0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  byte *local_14;
  byte *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x518) != 0) {
    local_c = *(int *)(param_1 + 0x518);
    if ((*(int *)(local_c + 8) == 0) &&
       (iVar2 = FUN__text__00424f80("list->data",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618fa4 + 10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_14 = *(byte **)(local_c + 8);
    local_18 = 0;
    local_1c = *local_14 - 1;
    local_10 = local_14;
    switch(local_1c) {
    case 0:
      local_18 = FUN__text__0048e5d0(param_1,local_14);
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                  DAT_00618fa4 + 0x24,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 2:
      local_18 = FUN__text__0048e6d0(param_1,local_14);
      break;
    case 3:
      local_18 = FUN__text__0048e790(param_1,local_14);
      break;
    case 4:
      local_18 = FUN__text__0048e990(param_1,local_14);
      break;
    case 8:
      local_18 = FUN__text__0048e9f0(param_1,local_14);
      break;
    case 9:
      local_18 = FUN__text__0048ea40(param_1,local_14);
      break;
    case 10:
      local_18 = FUN__text__0048ea90(param_1,local_14);
      break;
    case 0xb:
      local_18 = 0;
      break;
    case 0xc:
      local_18 = FUN__text__0048eda0(param_1,local_14);
      break;
    case 0xd:
      local_18 = FUN__text__0048ef60(param_1,local_14);
      break;
    case 0x10:
      local_18 = FUN__text__0048f0b0(param_1,local_14);
    }
    if (local_18 != 0) {
      FUN__text__0048dee0(param_1);
    }
  }
  local_8 = 0x48e47d;
  FUN__text__0056ce80();
  return;
}

