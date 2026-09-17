
void FUN__text__00442090(void)

{
  code *pcVar1;
  char cVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  undefined4 *local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_64;
  for (iVar3 = 0x18; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  cVar2 = FUN__text__0041ad60();
  local_18 = (int)cVar2;
  iVar3 = FUN__text__00419450();
  if (iVar3 == 0) {
    _memset((void *)(local_8 + 0x5330),0,0x3720);
    local_20 = local_8 + 0x5350;
    local_14 = 0;
    for (local_c = 0; local_c != 0x1e; local_c = local_c + 1) {
      if ((*(char *)(local_8 + 0x1ab0 + local_c * 8) != '\0') &&
         (*(char *)(local_8 + 0x1ab1 + local_c * 8) != '\0')) {
        local_1c = *(undefined4 **)(local_8 + 0x1ab4 + local_c * 8);
        puVar4 = local_1c;
        puVar5 = (undefined4 *)(local_20 + local_14 * 0xb0);
        for (iVar3 = 0x2c; iVar3 != 0; iVar3 = iVar3 + -1) {
          *puVar5 = *puVar4;
          puVar4 = puVar4 + 1;
          puVar5 = puVar5 + 1;
        }
        *(ushort *)(local_20 + local_14 * 0xb0) = (ushort)(byte)((char)local_18 + 1);
        *(char *)(local_8 + 0x53f4 + local_14 * 0xb0) = (char)local_18;
        local_14 = local_14 + 1;
        if (0x14 < local_14) break;
      }
    }
    if (((local_14 < 1) || (0x14 < local_14)) &&
       (iVar3 = FUN__text__00424f80("(0<cnt)&&(cnt<=20)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                    DAT_005ffc80 + 0x27,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_24 = local_14 * 0xb0 + 0x20;
    *(undefined1 *)(local_8 + 0x533d) = 6;
    *(undefined1 *)(local_8 + 0x5340) = (undefined1)local_14;
    local_10 = FUN__text__00419f90(local_8 + 0x5330,local_24);
    if ((local_10 != 0) &&
       (iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                    DAT_005ffc80 + 0x2f,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    local_20 = local_8 + 0x1c30;
    local_14 = 0;
    for (local_c = 0; local_c != 0x1e; local_c = local_c + 1) {
      if ((*(char *)(local_8 + 0x1ab0 + local_c * 8) != '\0') &&
         (*(char *)(local_8 + 0x1ab1 + local_c * 8) != '\0')) {
        local_1c = *(undefined4 **)(local_8 + 0x1ab4 + local_c * 8);
        puVar4 = local_1c;
        puVar5 = (undefined4 *)(local_20 + local_14 * 0xb0);
        for (iVar3 = 0x2c; iVar3 != 0; iVar3 = iVar3 + -1) {
          *puVar5 = *puVar4;
          puVar4 = puVar4 + 1;
          puVar5 = puVar5 + 1;
        }
        *(ushort *)(local_20 + local_14 * 0xb0) = (ushort)(byte)((char)local_18 + 1);
        *(char *)(local_8 + 0x1cd4 + local_14 * 0xb0) = (char)local_18;
        local_14 = local_14 + 1;
        if (0x14 < local_14) break;
      }
    }
    *(undefined1 *)(local_8 + local_18 + 0x1a91) = 1;
  }
  local_8 = 0x442355;
  FUN__text__0056ce80();
  return;
}

