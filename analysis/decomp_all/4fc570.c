
void __fastcall FUN__text__004fc570(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x39) == '\x01') {
    *(undefined *)(param_1 + 0x69) = (&DAT_00757940)[*(byte *)(param_1 + 0x51)];
    *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
    if (0x1e < *(byte *)(param_1 + 0x51)) {
      *(undefined1 *)(param_1 + 0x51) = 0;
      *(undefined1 *)(param_1 + 0x39) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_001_01.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x3a) == '\x01') {
    *(undefined *)(local_8 + 0x6a) = (&DAT_00757940)[*(byte *)(local_8 + 0x52)];
    *(char *)(local_8 + 0x52) = *(char *)(local_8 + 0x52) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x52)) {
      *(undefined1 *)(local_8 + 0x52) = 0;
      *(undefined1 *)(local_8 + 0x3a) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_001_02.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x3b) == '\x01') {
    *(undefined *)(local_8 + 0x6b) = (&DAT_00757940)[*(byte *)(local_8 + 0x53)];
    *(char *)(local_8 + 0x53) = *(char *)(local_8 + 0x53) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x53)) {
      *(undefined1 *)(local_8 + 0x53) = 0;
      *(undefined1 *)(local_8 + 0x3b) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_001_03.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x3c) == '\x01') {
    *(undefined *)(local_8 + 0x6c) = (&DAT_00757940)[*(byte *)(local_8 + 0x54)];
    *(char *)(local_8 + 0x54) = *(char *)(local_8 + 0x54) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x54)) {
      *(undefined1 *)(local_8 + 0x54) = 0;
      *(undefined1 *)(local_8 + 0x3c) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_002_01.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x3d) == '\x01') {
    *(undefined *)(local_8 + 0x6d) = (&DAT_00757940)[*(byte *)(local_8 + 0x55)];
    *(char *)(local_8 + 0x55) = *(char *)(local_8 + 0x55) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x55)) {
      *(undefined1 *)(local_8 + 0x55) = 0;
      *(undefined1 *)(local_8 + 0x3d) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_002_02.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x3e) == '\x01') {
    *(undefined *)(local_8 + 0x6e) = (&DAT_00757940)[*(byte *)(local_8 + 0x56)];
    *(char *)(local_8 + 0x56) = *(char *)(local_8 + 0x56) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x56)) {
      *(undefined1 *)(local_8 + 0x56) = 0;
      *(undefined1 *)(local_8 + 0x3e) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_003_01.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x3f) == '\x01') {
    *(undefined *)(local_8 + 0x6f) = (&DAT_00757940)[*(byte *)(local_8 + 0x57)];
    *(char *)(local_8 + 0x57) = *(char *)(local_8 + 0x57) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x57)) {
      *(undefined1 *)(local_8 + 0x57) = 0;
      *(undefined1 *)(local_8 + 0x3f) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_004_01.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x40) == '\x01') {
    *(undefined *)(local_8 + 0x70) = (&DAT_00757940)[*(byte *)(local_8 + 0x58)];
    *(char *)(local_8 + 0x58) = *(char *)(local_8 + 0x58) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x58)) {
      *(undefined1 *)(local_8 + 0x58) = 0;
      *(undefined1 *)(local_8 + 0x40) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_004_02.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x41) == '\x01') {
    *(undefined *)(local_8 + 0x71) = (&DAT_00757940)[*(byte *)(local_8 + 0x59)];
    *(char *)(local_8 + 0x59) = *(char *)(local_8 + 0x59) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x59)) {
      *(undefined1 *)(local_8 + 0x59) = 0;
      *(undefined1 *)(local_8 + 0x41) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_005_01.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  if (*(char *)(local_8 + 0x42) == '\x01') {
    *(undefined *)(local_8 + 0x72) = (&DAT_00757940)[*(byte *)(local_8 + 0x5a)];
    *(char *)(local_8 + 0x5a) = *(char *)(local_8 + 0x5a) + '\x01';
    if (0x1e < *(byte *)(local_8 + 0x5a)) {
      *(undefined1 *)(local_8 + 0x5a) = 0;
      *(undefined1 *)(local_8 + 0x42) = 2;
      uVar4 = 0;
      uVar1 = FUN__text__004501d0("data\\sound\\voice\\v098\\v098_005_02.mp3");
      FUN__text__0041e190(uVar1,uVar4);
    }
  }
  local_8 = 0x4fca04;
  FUN__text__0056ce80();
  return;
}

