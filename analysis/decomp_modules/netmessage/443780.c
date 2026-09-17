
void FUN__text__00443780(int *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  uint local_28;
  int local_24;
  undefined1 *local_20;
  int local_1c;
  int local_18;
  int local_14;
  int *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0041ae70();
  if (*param_1 == 0) {
    local_10 = (int *)param_1[2];
    local_24 = *local_10;
    if (((local_24 != 3) && (local_24 != 5)) && (local_24 != 0x31)) {
      FUN__text__0041b200(0,0,param_1[2]);
    }
  }
  else {
    local_14 = param_1[2];
    local_28 = (uint)*(byte *)(local_14 + 0xd);
    switch(local_28) {
    case 0:
      break;
    case 1:
      break;
    case 2:
      FUN__text__00442ce0(param_1);
      break;
    case 3:
      break;
    case 4:
      break;
    case 5:
      local_18 = param_1[2];
      local_1c = (int)*(short *)(local_8 + 0x1a88);
      *(undefined2 *)(local_8 + 0x1a88) = *(undefined2 *)(local_18 + 0x10);
      local_20 = (undefined1 *)FUN__text__0044c200((int)*(short *)(local_18 + 0x10));
      *(undefined1 *)(local_8 + 0x1a8b) = *local_20;
      FUN__text__00449fd0();
      FUN__text__0044ba50(local_1c,(int)*(short *)(local_8 + 0x1a88));
      FUN__text__00442950();
      break;
    case 6:
      FUN__text__00442690(param_1);
      break;
    case 7:
      FUN__text__00442a50(param_1);
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffca8 + 0x6a,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 9:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffca8 + 0x4d,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 10:
      break;
    case 0xb:
      FUN__text__004432f0(param_1);
      break;
    case 0xc:
      *(undefined1 *)(local_c + 1) = 1;
      break;
    case 0xd:
      FUN__text__00443080(param_1);
      break;
    case 0x10:
    }
  }
  local_8 = 0x443980;
  FUN__text__0056ce80();
  return;
}

