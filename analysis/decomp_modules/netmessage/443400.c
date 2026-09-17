
void FUN__text__00443400(int *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_908 [16];
  uint local_8c8;
  int local_8c4;
  int local_8c0;
  int local_8bc;
  undefined1 local_8b8 [13];
  undefined1 local_8ab;
  undefined1 local_8a8;
  undefined4 auStack_8a4 [544];
  int local_24;
  int local_20;
  int *local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_908;
  for (iVar2 = 0x241; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0041ae70();
  if (*param_1 == 0) {
    local_1c = (int *)param_1[2];
    local_8c4 = *local_1c;
    if (local_8c4 == 3) {
      local_20 = param_1[2];
      FUN__text__0041afd0(*(undefined4 *)(local_20 + 0x20),*(undefined4 *)(local_20 + 8));
      FUN__text__0044b610();
      local_14 = FUN__text__00442b30();
      local_14 = FUN__text__00441fe0();
      local_14 = FUN__text__004429a0();
    }
    else if (local_8c4 == 5) {
      local_24 = param_1[2];
      FUN__text__0041b0f0(*(undefined4 *)(local_24 + 8));
      FUN__text__0044b610();
      _memset(local_8b8,0,0x894);
      local_8ab = 2;
      local_8a8 = FUN__text__0041aea0();
      for (local_18 = 0; local_18 != 0x10; local_18 = local_18 + 1) {
        puVar3 = (undefined4 *)(local_c + local_18 * 0x88);
        puVar4 = auStack_8a4 + local_18 * 0x22;
        for (iVar2 = 0x22; iVar2 != 0; iVar2 = iVar2 + -1) {
          *puVar4 = *puVar3;
          puVar3 = puVar3 + 1;
          puVar4 = puVar4 + 1;
        }
      }
      local_10 = 0x894;
      local_14 = FUN__text__00419fe0(local_8b8,0x894);
      if ((local_14 != 0) &&
         (iVar2 = FUN__text__00424f80("ret==((HRESULT)0x00000000L)",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                      DAT_005ffca4 + 0x38,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  else {
    local_8bc = param_1[2];
    local_8c8 = (uint)*(byte *)(local_8bc + 0xd);
    switch(local_8c8) {
    case 0:
      break;
    case 1:
      break;
    case 2:
      local_8c0 = param_1[2];
      break;
    case 3:
      FUN__text__00441ea0(param_1);
      break;
    case 4:
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffca4 + 0x92,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 6:
      FUN__text__00442580(param_1);
      break;
    case 7:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffca4 + 0x7f,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 9:
      FUN__text__004428b0(*param_1);
      break;
    case 10:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                  DAT_005ffca4 + 0x7b,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 0xb:
      FUN__text__004432f0(param_1);
      break;
    case 0xd:
      FUN__text__00443080(param_1);
      break;
    case 0xe:
      FUN__text__00442e50(param_1);
      break;
    case 0x10:
    }
  }
  local_8 = 0x443729;
  FUN__text__0056ce80();
  return;
}

