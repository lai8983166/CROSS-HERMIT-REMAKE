
void FUN__text__0047f6b0(undefined4 param_1,int param_2,int param_3,undefined4 param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)FUN__text__0047a8e0(param_2);
  local_10 = param_3;
  switch(param_3) {
  case 0:
    *(char *)(*(int *)(param_2 + 600) + 0x9f) = (char)param_4;
    break;
  case 1:
    *(char *)(*(int *)(param_2 + 600) + 0xa0) = (char)param_4;
    break;
  case 2:
    *(char *)(*(int *)(param_2 + 600) + 0xa2) = (char)param_4;
    break;
  case 3:
    *local_c = (char)param_4;
    break;
  case 4:
    local_c[1] = (char)param_4;
    break;
  case 5:
    *(undefined4 *)(local_c + 4) = param_4;
    break;
  case 6:
    *(undefined4 *)(local_c + 8) = param_4;
    break;
  case 7:
    *(undefined4 *)(local_c + 0xc) = param_4;
    break;
  case 8:
    local_c[0x10] = (char)param_4;
    break;
  case 9:
    local_c[0x11] = (char)param_4;
    break;
  case 10:
    local_c[0x12] = (char)param_4;
    break;
  case 0xb:
    local_c[0x13] = (char)param_4;
    break;
  case 0xc:
    local_c[0x14] = (char)param_4;
    break;
  case 0xd:
    local_c[0x15] = (char)param_4;
    break;
  case 0xe:
    local_c[0x16] = (char)param_4;
    break;
  case 0xf:
    local_c[0x17] = (char)param_4;
    break;
  case 0x10:
    local_c[0x18] = (char)param_4;
    break;
  case 0x11:
    local_c[0x19] = (char)param_4;
    break;
  case 0x12:
    local_c[0x1a] = (char)param_4;
    break;
  case 0x13:
    local_c[0x1b] = (char)param_4;
    break;
  case 0x14:
    local_c[0x1c] = (char)param_4;
    break;
  case 0x15:
    local_c[0x1d] = (char)param_4;
    break;
  case 0x16:
    local_c[0x1e] = (char)param_4;
    break;
  case 0x17:
    *(undefined4 *)(local_c + 0x20) = param_4;
    break;
  case 0x18:
    local_c[0x24] = (char)param_4;
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e84 + 0x21,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_14 = param_3;
  if (param_3 == 1) {
    if ((*(char *)(*(int *)(param_2 + 600) + 0xa0) == '\0') && (*local_c == '\x01')) {
      *(undefined1 *)(param_2 + 0x2a9) = 0;
    }
  }
  else if (param_3 == 2) {
    *(undefined1 *)(param_2 + 0x2a9) = 0;
  }
  else if (((param_3 == 3) && (*(char *)(*(int *)(param_2 + 600) + 0xa0) == '\0')) &&
          (*local_c == '\x01')) {
    *(undefined1 *)(param_2 + 0x2a9) = 0;
  }
  local_8 = 0x47f911;
  FUN__text__0056ce80();
  return;
}

