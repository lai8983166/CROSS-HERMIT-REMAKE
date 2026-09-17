
void FUN__text__00476680(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_80 [16];
  int local_40;
  undefined4 local_3c;
  int local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  int local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  int local_18;
  char *local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_80;
  for (iVar2 = 0x1f; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_14 = (char *)(param_1 + 0x293 + param_2);
  if (*(short *)(param_1 + 0x4e0) != 0) {
    *(short *)(param_1 + 0x4e0) = *(short *)(param_1 + 0x4e0) + -1;
    goto switchD__text__00476709_default;
  }
  local_10 = (char *)FUN__text__0047a8e0(param_1);
  local_18 = (int)*local_14;
  switch(local_18) {
  case 0:
    local_10[0x2c] = '\0';
    local_10[0x2d] = '\0';
    local_10[0x2e] = '\0';
    local_10[0x2f] = '\0';
    local_10[0x30] = '\0';
    local_10[0x31] = '\0';
    local_10[0x32] = '\0';
    local_10[0x33] = '\0';
    iVar2 = FUN__text__004698a0(param_1);
    if ((((iVar2 != 0) && (*local_10 != '\x01')) &&
        ((*(char *)(*(int *)(param_1 + 600) + 0x9f) == '\x02' ||
         (*(char *)(*(int *)(param_1 + 600) + 0x9f) == '\x03')))) ||
       (*(char *)(*(int *)(param_1 + 600) + 0x30) == '\x04')) break;
    local_1c = FUN__text__0047d210(param_1,0);
    switch(local_1c) {
    case 0:
      goto switchD__text__004767b6_caseD_0;
    case 1:
      *local_14 = '\x03';
      goto switchD__text__00476709_caseD_3;
    case 2:
      *local_14 = '\x01';
      break;
    case 3:
      *local_14 = '\x02';
      break;
    case 4:
      break;
    case 5:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e00 + 0x31,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    break;
  case 1:
    local_20 = FUN__text__0047d570(param_1,0);
    switch(local_20) {
    case 0:
switchD__text__004767b6_caseD_0:
      goto switchD__text__00476709_default;
    case 1:
      *local_14 = '\x03';
      goto switchD__text__00476709_caseD_3;
    case 3:
      *local_14 = '\x02';
      break;
    case 4:
      goto switchD__text__00476709_default;
    case 5:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e00 + 0x3c,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    break;
  case 2:
    local_24 = FUN__text__0047d730(param_1,0);
    switch(local_24) {
    case 0:
      goto switchD__text__004767b6_caseD_0;
    case 1:
      *local_14 = '\x03';
      goto switchD__text__00476709_caseD_3;
    case 2:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e00 + 0x44,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 4:
      goto switchD__text__00476709_default;
    case 5:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e00 + 0x47,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    break;
  case 3:
switchD__text__00476709_caseD_3:
    local_28 = FUN__text__0047d830(param_1);
    if (local_28 == 0) {
      *local_14 = '\x04';
    }
    else if ((local_28 != 1) && (local_28 == 2)) {
      *local_14 = '\0';
    }
    break;
  case 4:
    local_2c = FUN__text__0047d210(param_1,1);
    switch(local_2c) {
    case 0:
      iVar2 = FUN__text__00468d80(param_1);
      if (iVar2 == 0) {
        *(undefined2 *)(param_1 + 0x4e0) = 0xb4;
      }
      else {
        *(undefined2 *)(param_1 + 0x4e0) = 0x1e;
      }
      break;
    case 1:
      *local_14 = '\a';
      goto switchD__text__00476709_caseD_7;
    case 2:
      *local_14 = '\x05';
      break;
    case 3:
      *local_14 = '\x06';
      break;
    case 4:
      *local_14 = '\x03';
      break;
    case 5:
    }
    break;
  case 5:
    local_30 = FUN__text__0047d570(param_1,1);
    switch(local_30) {
    case 0:
      iVar2 = FUN__text__00468d80(param_1);
      if (iVar2 == 0) {
        *(undefined2 *)(param_1 + 0x4e0) = 0xb4;
      }
      else {
        *(undefined2 *)(param_1 + 0x4e0) = 0x1e;
      }
      break;
    case 1:
      *local_14 = '\a';
      goto switchD__text__00476709_caseD_7;
    case 3:
      *local_14 = '\x06';
      break;
    case 4:
      *local_14 = '\x03';
      break;
    case 5:
      goto switchD__text__00476709_default;
    }
    break;
  case 6:
    local_34 = FUN__text__0047d730(param_1,1);
    switch(local_34) {
    case 0:
      iVar2 = FUN__text__00468d80(param_1);
      if (iVar2 == 0) {
        *(undefined2 *)(param_1 + 0x4e0) = 0xb4;
      }
      else {
        *(undefined2 *)(param_1 + 0x4e0) = 0x1e;
      }
      break;
    case 1:
      *local_14 = '\a';
      goto switchD__text__00476709_caseD_7;
    case 2:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e00 + 0x89,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 4:
      *local_14 = '\x03';
      break;
    case 5:
      goto switchD__text__00476709_default;
    }
    break;
  case 7:
switchD__text__00476709_caseD_7:
    FUN__text__0047d930(param_1);
    *local_14 = *local_14 + '\x01';
  case 8:
switchD__text__00476709_caseD_8:
    local_38 = FUN__text__0047da30(param_1);
    if (local_38 == 0) {
      *local_14 = *local_14 + '\x01';
    }
    else if ((local_38 != 1) && (local_38 == 2)) {
      *local_14 = '\x04';
      iVar2 = FUN__text__00468d80(param_1);
      if (iVar2 == 0) {
        *(undefined2 *)(param_1 + 0x4e0) = 0x1e;
      }
      else {
        *(undefined2 *)(param_1 + 0x4e0) = 0;
      }
    }
    break;
  case 9:
    local_3c = FUN__text__0047dbd0(param_1);
    switch(local_3c) {
    case 0:
      local_40 = FUN__text__0047dec0(param_1);
      local_40 = local_40 + -1;
      switch(local_40) {
      case 0:
        *local_14 = '\x04';
        iVar2 = FUN__text__00468d80(param_1);
        if (iVar2 == 0) {
          *(undefined2 *)(param_1 + 0x4e0) = 0x1e;
        }
        else {
          *(undefined2 *)(param_1 + 0x4e0) = 0;
        }
        break;
      case 1:
        local_10[0x30] = '\0';
        local_10[0x31] = '\0';
        local_10[0x32] = '\0';
        local_10[0x33] = '\0';
        if (*(int *)(local_10 + 8) != 0) {
          FUN__text__0046bcc0(param_1,1);
          *local_14 = '\n';
        }
        break;
      case 2:
        *local_14 = '\0';
        iVar2 = FUN__text__00468d80(param_1);
        if (iVar2 == 0) {
          *(undefined2 *)(param_1 + 0x4e0) = 0x3c;
        }
        else {
          *(undefined2 *)(param_1 + 0x4e0) = 0x1e;
        }
        break;
      case 3:
      }
      break;
    case 1:
      *local_14 = '\x03';
      break;
    case 2:
      *local_14 = '\x04';
      break;
    case 3:
      *local_14 = '\a';
      goto switchD__text__00476709_caseD_7;
    case 4:
      *local_14 = '\b';
      goto switchD__text__00476709_caseD_8;
    }
    break;
  case 10:
    iVar2 = FUN__text__0047e2b0(param_1);
    if (iVar2 != 0) {
      *local_14 = '\t';
    }
  }
switchD__text__00476709_default:
  local_8 = 0x476ce0;
  FUN__text__0056ce80();
  return;
}

