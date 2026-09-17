
void FUN__text__00475460(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)(param_1 + 0x290);
  if (*(char *)(param_1 + 0x2a6) == '\0') {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618df4 + 0x42,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    *(undefined4 *)local_c = *(undefined4 *)(param_1 + 0x29b);
    *(undefined4 *)(param_1 + 0x294) = *(undefined4 *)(param_1 + 0x29f);
    *(undefined2 *)(param_1 + 0x298) = *(undefined2 *)(param_1 + 0x2a3);
    *(undefined1 *)(param_1 + 0x29a) = *(undefined1 *)(param_1 + 0x2a5);
    local_10 = (int)*local_c;
    switch(local_10) {
    case 0:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618df4 + 8,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 7:
    case 8:
    case 9:
    case 10:
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x10:
    case 0x11:
    case 0x12:
    case 0x13:
    case 0x14:
    case 0x15:
    case 0x16:
    case 0x17:
    case 0x18:
    case 0x19:
    case 0x1a:
    case 0x1b:
    case 0x1c:
      FUN__text__00475270(param_1,(int)*local_c);
      break;
    case 6:
      if (*(short *)(param_1 + 0x4f2) == -1) {
        FUN__text__00475270(param_1,0xf);
      }
      else if (*(char *)(param_1 + 0x293) < '\x17') {
        FUN__text__00475270(param_1,(int)*local_c);
      }
      else {
        FUN__text__00475270(param_1,0xf);
      }
      break;
    case 0x1d:
      if (*(short *)(param_1 + 0x4ee) == -1) {
        FUN__text__00475270(param_1,0xf);
      }
      else {
        FUN__text__00475270(param_1,(int)*local_c);
      }
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_0059d380,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618df4 + 0x3b,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    local_c[0x16] = '\0';
  }
  local_8 = 0x475618;
  FUN__text__0056ce80();
  return;
}

