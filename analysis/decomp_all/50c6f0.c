
void __fastcall FUN__text__0050c6f0(int param_1)

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
           (ushort)(byte)(&DAT_0075add0)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) +
           (ushort)(byte)(&DAT_0075add1)[(uint)*(byte *)(param_1 + 0x51) * 2];
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
           (ushort)(byte)(&DAT_0075ac9c)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(ushort *)(param_1 + 0x9e) =
           *(short *)(param_1 + 0x9e) -
           (ushort)(byte)(&DAT_0075ac9d)[(uint)*(byte *)(param_1 + 0x52) * 2];
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
           (ushort)(byte)(&DAT_0075aba4)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) -
           (ushort)(byte)(&DAT_0075aba5)[(uint)*(byte *)(param_1 + 0x51) * 2];
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
           (ushort)(byte)(&DAT_0075aaa4)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(ushort *)(param_1 + 0x9e) =
           *(short *)(param_1 + 0x9e) -
           (ushort)(byte)(&DAT_0075aaa5)[(uint)*(byte *)(param_1 + 0x52) * 2];
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
           *(short *)(param_1 + 0x82) + (ushort)(byte)(&DAT_0075b9f4)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) + (ushort)(byte)(&DAT_0075ba0c)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) != '\0') {
      *(ushort *)(param_1 + 0x86) =
           *(short *)(param_1 + 0x86) + (ushort)(byte)(&DAT_0075ba24)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) != '\0') {
      *(ushort *)(param_1 + 0x88) =
           *(short *)(param_1 + 0x88) + (ushort)(byte)(&DAT_0075ba40)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) != '\0') {
      *(ushort *)(param_1 + 0x8a) =
           *(short *)(param_1 + 0x8a) + (ushort)(byte)(&DAT_0075ba58)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) != '\0') {
      *(ushort *)(param_1 + 0x8c) =
           *(short *)(param_1 + 0x8c) + (ushort)(byte)(&DAT_0075ba70)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3f) != '\0') {
      *(ushort *)(param_1 + 0x8e) =
           *(short *)(param_1 + 0x8e) + (ushort)(byte)(&DAT_0075ba88)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) != '\0') {
      *(ushort *)(param_1 + 0x90) =
           *(short *)(param_1 + 0x90) + (ushort)(byte)(&DAT_0075baa0)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 0;
        *(undefined1 *)(param_1 + 0x37) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 10;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) + (ushort)(byte)(&DAT_0075a9c8)[*(byte *)(param_1 + 0x51)];
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
           (ushort)(byte)(&DAT_0075a7d4)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) +
           (ushort)(byte)(&DAT_0075a7d5)[(uint)*(byte *)(param_1 + 0x51) * 2];
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
           *(short *)(param_1 + 0x84) - (ushort)(byte)(&DAT_0075af94)[*(byte *)(param_1 + 0x52)];
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
           (ushort)(byte)(&DAT_0075affc)[(uint)*(byte *)(param_1 + 0x55) * 2];
      *(ushort *)(param_1 + 0xa4) =
           *(short *)(param_1 + 0xa4) -
           (ushort)(byte)(&DAT_0075affd)[(uint)*(byte *)(param_1 + 0x55) * 2];
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
           *(short *)(param_1 + 0x8c) - (ushort)(byte)(&DAT_0075a8e0)[*(byte *)(param_1 + 0x56)];
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
        *(undefined1 *)(param_1 + 0x30) = 0xc;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) -
           (ushort)(byte)(&DAT_0075a700)[(uint)*(byte *)(param_1 + 0x52) * 2];
      *(ushort *)(param_1 + 0x9e) =
           *(short *)(param_1 + 0x9e) -
           (ushort)(byte)(&DAT_0075a701)[(uint)*(byte *)(param_1 + 0x52) * 2];
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
           (ushort)(byte)(&DAT_0075a648)[(uint)*(byte *)(param_1 + 0x53) * 2];
      *(ushort *)(param_1 + 0xa0) =
           *(short *)(param_1 + 0xa0) -
           (ushort)(byte)(&DAT_0075a649)[(uint)*(byte *)(param_1 + 0x53) * 2];
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
    break;
  case 10:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x82) =
           *(short *)(param_1 + 0x82) +
           (ushort)(byte)(&DAT_0075a54c)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(ushort *)(param_1 + 0x9c) =
           *(short *)(param_1 + 0x9c) -
           (ushort)(byte)(&DAT_0075a54d)[(uint)*(byte *)(param_1 + 0x51) * 2];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (*(char *)(param_1 + 0x51) == '\x1c') {
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
      if (*(char *)(param_1 + 0x51) == '`') {
        *(undefined1 *)(param_1 + 0x39) = 3;
      }
      if (0x7c < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(ushort *)(param_1 + 0x82) =
           *(short *)(param_1 + 0x82) - (ushort)(byte)(&DAT_0075a478)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (*(char *)(param_1 + 0x51) == '\x19') {
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
      if (0x58 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(ushort *)(param_1 + 0x84) =
           *(short *)(param_1 + 0x84) - (ushort)(byte)(&DAT_0075a4d4)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (*(char *)(param_1 + 0x52) == '!') {
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
      if (*(char *)(param_1 + 0x52) == 'D') {
        *(undefined1 *)(param_1 + 0x3a) = 3;
      }
      if (0x74 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) != '\0') {
      *(ushort *)(param_1 + 0x86) =
           *(short *)(param_1 + 0x86) -
           (ushort)(byte)(&DAT_0075a41c)[(uint)*(byte *)(param_1 + 0x53) * 2];
      *(ushort *)(param_1 + 0xa0) =
           *(short *)(param_1 + 0xa0) +
           (ushort)(byte)(&DAT_0075a41d)[(uint)*(byte *)(param_1 + 0x53) * 2];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x2c < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) != '\0') {
      *(ushort *)(param_1 + 0x88) =
           *(short *)(param_1 + 0x88) +
           (ushort)(byte)(&DAT_0075a3c0)[(uint)*(byte *)(param_1 + 0x54) * 2];
      *(ushort *)(param_1 + 0xa2) =
           *(short *)(param_1 + 0xa2) +
           (ushort)(byte)(&DAT_0075a3c1)[(uint)*(byte *)(param_1 + 0x54) * 2];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) != '\0') {
      *(ushort *)(param_1 + 0x8a) =
           *(short *)(param_1 + 0x8a) +
           (ushort)(byte)(&DAT_0075a96c)[(uint)*(byte *)(param_1 + 0x55) * 2];
      *(ushort *)(param_1 + 0xa4) =
           *(short *)(param_1 + 0xa4) +
           (ushort)(byte)(&DAT_0075a96d)[(uint)*(byte *)(param_1 + 0x55) * 2];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x2c < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) != '\0') {
      *(ushort *)(param_1 + 0x8c) =
           *(short *)(param_1 + 0x8c) -
           (ushort)(byte)(&DAT_0075a368)[(uint)*(byte *)(param_1 + 0x56) * 2];
      *(ushort *)(param_1 + 0xa6) =
           *(short *)(param_1 + 0xa6) +
           (ushort)(byte)(&DAT_0075a369)[(uint)*(byte *)(param_1 + 0x56) * 2];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x2b < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
  }
  return;
}

