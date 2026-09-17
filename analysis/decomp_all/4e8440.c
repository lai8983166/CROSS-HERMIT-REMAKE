
void __fastcall FUN__text__004e8440(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(*(undefined1 *)(param_1 + 0x34)) {
  case 3:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x82) =
           *(short *)(param_1 + 0x82) +
           (ushort)(byte)(&DAT_00754f4c)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) +
           (ushort)(byte)(&DAT_00754f4d)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (*(char *)(param_1 + 0x51) == '2') {
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
      if (*(char *)(param_1 + 0x51) == -0x65) {
        *(undefined1 *)(param_1 + 0x39) = 3;
      }
      if (0xb2 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) -
           (ushort)(byte)(&DAT_00754e18)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(ushort *)(param_1 + 0x9e) =
           *(short *)(param_1 + 0x9e) -
           (ushort)(byte)(&DAT_00754e19)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (*(char *)(param_1 + 0x52) == '!') {
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
      if (*(char *)(param_1 + 0x52) == -0x7a) {
        *(undefined1 *)(param_1 + 0x3a) = 3;
      }
      if (0x98 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x82) =
           *(short *)(param_1 + 0x82) +
           (ushort)(byte)(&DAT_00754d20)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) -
           (ushort)(byte)(&DAT_00754d21)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (*(char *)(param_1 + 0x51) == '\x1b') {
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
      if (*(char *)(param_1 + 0x51) == 'D') {
        *(undefined1 *)(param_1 + 0x39) = 3;
      }
      if (0x7a < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) -
           (ushort)(byte)(&DAT_00754c20)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(ushort *)(param_1 + 0x9e) =
           *(short *)(param_1 + 0x9e) -
           (ushort)(byte)(&DAT_00754c21)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (*(char *)(param_1 + 0x52) == '\x11') {
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
      if (*(char *)(param_1 + 0x52) == 'V') {
        *(undefined1 *)(param_1 + 0x3a) = 3;
      }
      if (0x7e < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x82) =
           *(short *)(param_1 + 0x82) + (ushort)(byte)(&DAT_00755b70)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) + (ushort)(byte)(&DAT_00755b88)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) != '\0') {
      *(ushort *)(param_1 + 0x86) =
           *(short *)(param_1 + 0x86) + (ushort)(byte)(&DAT_00755ba0)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) != '\0') {
      *(ushort *)(param_1 + 0x88) =
           *(short *)(param_1 + 0x88) + (ushort)(byte)(&DAT_00755bbc)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) != '\0') {
      *(ushort *)(param_1 + 0x8a) =
           *(short *)(param_1 + 0x8a) + (ushort)(byte)(&DAT_00755bd4)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) != '\0') {
      *(ushort *)(param_1 + 0x8c) =
           *(short *)(param_1 + 0x8c) + (ushort)(byte)(&DAT_00755bec)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3f) != '\0') {
      *(ushort *)(param_1 + 0x8e) =
           *(short *)(param_1 + 0x8e) + (ushort)(byte)(&DAT_00755c04)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) != '\0') {
      *(ushort *)(param_1 + 0x90) =
           *(short *)(param_1 + 0x90) + (ushort)(byte)(&DAT_00755c1c)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 0;
        *(undefined1 *)(param_1 + 0x37) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x32) = 10;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) + (ushort)(byte)(&DAT_00754b44)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (*(char *)(param_1 + 0x51) == '<') {
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
      if (*(char *)(param_1 + 0x51) == -0x4d) {
        *(undefined1 *)(param_1 + 0x39) = 3;
      }
      if (0xdb < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x82) =
           *(short *)(param_1 + 0x82) +
           (ushort)(byte)(&DAT_00754950)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) +
           (ushort)(byte)(&DAT_00754951)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (*(char *)(param_1 + 0x51) == '\x14') {
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
      if (*(char *)(param_1 + 0x51) == 'j') {
        *(undefined1 *)(param_1 + 0x39) = 3;
      }
      if (0x85 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) - (ushort)(byte)(&DAT_00755110)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (*(char *)(param_1 + 0x52) == '\x19') {
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
      if (*(char *)(param_1 + 0x52) == 'N') {
        *(undefined1 *)(param_1 + 0x3a) = 3;
      }
      if (0x67 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) != '\0') {
      *(ushort *)(param_1 + 0x8a) =
           *(short *)(param_1 + 0x8a) +
           (ushort)(byte)(&DAT_00755178)[(uint)*(byte *)(param_1 + 0x55) * 2];
      *(ushort *)(param_1 + 0xa4) =
           *(short *)(param_1 + 0xa4) -
           (ushort)(byte)(&DAT_00755179)[(uint)*(byte *)(param_1 + 0x55) * 2];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (*(char *)(param_1 + 0x55) == '\x1c') {
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
      if (*(char *)(param_1 + 0x55) == '~') {
        *(undefined1 *)(param_1 + 0x3d) = 3;
      }
      if (0x99 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) != '\0') {
      *(ushort *)(param_1 + 0x8c) =
           *(short *)(param_1 + 0x8c) - (ushort)(byte)(&DAT_00754a5c)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (*(char *)(param_1 + 0x56) == '\x1c') {
        *(undefined1 *)(param_1 + 0x3e) = 2;
      }
      if (*(char *)(param_1 + 0x56) == 'n') {
        *(undefined1 *)(param_1 + 0x3e) = 3;
      }
      if (0x89 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x32) = 0xc;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) -
           (ushort)(byte)(&DAT_0075487c)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(ushort *)(param_1 + 0x9e) =
           *(short *)(param_1 + 0x9e) -
           (ushort)(byte)(&DAT_0075487d)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (*(char *)(param_1 + 0x52) == '\x17') {
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
      if (*(char *)(param_1 + 0x52) == 'U') {
        *(undefined1 *)(param_1 + 0x3a) = 3;
      }
      if (0x69 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) != '\0') {
      *(ushort *)(param_1 + 0x86) =
           *(short *)(param_1 + 0x86) +
           (ushort)(byte)(&DAT_007547c4)[(uint)*(byte *)(param_1 + 0x53) * 2];
      *(ushort *)(param_1 + 0xa0) =
           *(short *)(param_1 + 0xa0) -
           (ushort)(byte)(&DAT_007547c5)[(uint)*(byte *)(param_1 + 0x53) * 2];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (*(char *)(param_1 + 0x53) == '\x18') {
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
      if (*(char *)(param_1 + 0x53) == 'H') {
        *(undefined1 *)(param_1 + 0x3b) = 3;
      }
      if (0x5a < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
  }
  return;
}

