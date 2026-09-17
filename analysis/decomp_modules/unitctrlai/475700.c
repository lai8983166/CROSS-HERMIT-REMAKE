
void FUN__text__00475700(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  uint local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)(param_1 + 0x290);
  FUN__text__004751f0(param_1);
  iVar2 = FUN__text__004697f0(param_1);
  if (iVar2 == 0) {
    local_18 = (int)*local_c;
    switch(local_18) {
    case 0:
    case 7:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618df8 + 0x7e,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 1:
    case 0x19:
      local_10 = FUN__text__00475d60(param_1);
      break;
    case 2:
      local_10 = FUN__text__00476250(param_1);
      break;
    case 3:
      local_10 = FUN__text__004763d0(param_1);
      break;
    case 4:
      local_10 = FUN__text__00476dd0(param_1);
      break;
    case 5:
      local_10 = 0;
      break;
    case 6:
      local_10 = FUN__text__00477980(param_1);
      break;
    case 8:
      local_10 = FUN__text__00478850(param_1);
      break;
    case 9:
      local_10 = FUN__text__00478bc0(param_1);
      break;
    case 10:
      local_10 = FUN__text__00479270(param_1);
      break;
    case 0xb:
      local_10 = FUN__text__00479f40(param_1);
      break;
    case 0xc:
      local_10 = FUN__text__00479820(param_1);
      break;
    case 0xd:
      local_10 = FUN__text__004799c0(param_1);
      break;
    case 0xe:
      local_10 = FUN__text__00479410(param_1);
      break;
    case 0xf:
      local_10 = FUN__text__00476470(param_1);
      break;
    case 0x10:
      local_10 = FUN__text__0047ed90(param_1);
      break;
    case 0x11:
      local_10 = FUN__text__00475f60(param_1);
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618df8 + 0xea,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 0x13:
      local_10 = FUN__text__004776a0(param_1);
      break;
    case 0x14:
      local_10 = FUN__text__0047a530(param_1);
      break;
    case 0x15:
      local_10 = FUN__text__0047a590(param_1);
      break;
    case 0x16:
      local_10 = FUN__text__0047a470(param_1);
      break;
    case 0x17:
      local_10 = FUN__text__004771d0(param_1);
      break;
    case 0x18:
      local_10 = FUN__text__0047f1d0(param_1);
      break;
    case 0x1a:
      local_10 = FUN__text__0047efb0(param_1);
      break;
    case 0x1b:
      local_10 = FUN__text__00479e40(param_1);
      break;
    case 0x1c:
      local_10 = FUN__text__004761c0(param_1);
      break;
    case 0x1d:
      local_10 = FUN__text__0047e680(param_1);
    }
  }
  else {
    local_14 = (int)*local_c;
    switch(local_14) {
    case 0:
    case 7:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618df8 + 0x10,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 1:
    case 0x19:
      local_10 = FUN__text__00475d60(param_1);
      break;
    case 2:
      local_10 = FUN__text__00476250(param_1);
      break;
    case 3:
      local_10 = FUN__text__004763d0(param_1);
      break;
    case 4:
      local_10 = FUN__text__00476dd0(param_1);
      break;
    case 5:
      local_10 = 0;
      break;
    case 6:
      local_10 = FUN__text__00477980(param_1);
      break;
    case 8:
      local_10 = FUN__text__00478850(param_1);
      break;
    case 9:
      local_10 = FUN__text__00478bc0(param_1);
      break;
    case 10:
      local_10 = FUN__text__00479270(param_1);
      break;
    case 0xb:
      local_10 = FUN__text__00479f40(param_1);
      break;
    case 0xc:
      local_10 = FUN__text__00479820(param_1);
      break;
    case 0xd:
      local_10 = FUN__text__004799c0(param_1);
      break;
    case 0xe:
      local_10 = FUN__text__00479410(param_1);
      break;
    case 0xf:
      local_10 = FUN__text__00476470(param_1);
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618df8 + 0x74,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 0x11:
      local_10 = FUN__text__00475f60(param_1);
      break;
    case 0x13:
      local_10 = FUN__text__004776a0(param_1);
      break;
    case 0x14:
      local_10 = FUN__text__0047a530(param_1);
      break;
    case 0x15:
      local_10 = FUN__text__0047a590(param_1);
      break;
    case 0x16:
      local_10 = FUN__text__0047a470(param_1);
      break;
    case 0x17:
      local_10 = FUN__text__004771d0(param_1);
      break;
    case 0x18:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618df8 + 0x6f,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 0x1b:
      local_10 = FUN__text__00479e40(param_1);
      break;
    case 0x1c:
      local_10 = FUN__text__004761c0(param_1);
      break;
    case 0x1d:
      local_10 = FUN__text__0047e680(param_1);
    }
  }
  local_1c = (uint)*(ushort *)(*(int *)(param_1 + 600) + 2);
  if ((0x182 < local_1c) && (local_1c < 0x197)) {
    FUN__text__00480a60(param_1);
  }
  local_8 = 0x475c65;
  FUN__text__0056ce80();
  return;
}

