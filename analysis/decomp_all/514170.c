
void __fastcall FUN__text__00514170(int param_1)

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
  case 1:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075cdb8)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075cdf0)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0xe < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 2;
      }
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075ce1c)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x12 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075ce44)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x12 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 2;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075ce6c)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x14 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075cea0)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075ced4)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x20 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075cf0c)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x23 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x01') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075cf44)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 2;
        *(undefined1 *)(param_1 + 0x30) = 8;
        *(undefined1 *)(param_1 + 0x35) = 4;
        *(undefined1 *)(param_1 + 0x34) = 4;
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075cf74)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075cfac)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x1e < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075cfe8)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x1e < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d024)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d05c)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d094)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075d0cc)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x01') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075d100)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 2;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x01') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075d138)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 2;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075d170)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 2;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d1a8)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d1dc)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x22 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075dbb0)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d21c)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x19 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075dbf0)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x3f) == '\x01') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075d254)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 2;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x01') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075dc20)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 2;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075dc50)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 2;
      }
    }
    break;
  case 0xc:
    if (*(char *)(param_1 + 0x50) == '\x01') {
      *(undefined *)(param_1 + 0x80) = (&DAT_0075d28c)[*(byte *)(param_1 + 0x68)];
      *(char *)(param_1 + 0x68) = *(char *)(param_1 + 0x68) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x68)) {
        *(undefined1 *)(param_1 + 0x68) = 0;
        *(undefined1 *)(param_1 + 0x50) = 2;
      }
    }
    break;
  case 0xd:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075dc80)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075dcb4)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    break;
  case 0xe:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d2c0)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d2f0)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075d320)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d350)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x46) == '\x01') {
      *(undefined *)(param_1 + 0x76) = (&DAT_0075d380)[*(byte *)(param_1 + 0x5e)];
      *(char *)(param_1 + 0x5e) = *(char *)(param_1 + 0x5e) + '\x01';
      if (0x51 < *(byte *)(param_1 + 0x5e)) {
        *(undefined1 *)(param_1 + 0x5e) = 0;
        *(undefined1 *)(param_1 + 0x46) = 0;
      }
    }
    if (*(char *)(param_1 + 0x42) == '\x01') {
      *(undefined *)(param_1 + 0x72) = (&DAT_0075d3d4)[*(byte *)(param_1 + 0x5a)];
      *(char *)(param_1 + 0x5a) = *(char *)(param_1 + 0x5a) + '\x01';
      if (0x2a < *(byte *)(param_1 + 0x5a)) {
        *(undefined1 *)(param_1 + 0x5a) = 0;
        *(undefined1 *)(param_1 + 0x42) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075d400)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x27 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075d428)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x2e < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 0;
      }
    }
    if (*(char *)(param_1 + 0x47) == '\x01') {
      *(undefined *)(param_1 + 0x77) = (&DAT_0075dce4)[*(byte *)(param_1 + 0x5f)];
      *(char *)(param_1 + 0x5f) = *(char *)(param_1 + 0x5f) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x5f)) {
        *(undefined1 *)(param_1 + 0x5f) = 0;
        *(undefined1 *)(param_1 + 0x47) = 2;
      }
    }
    if (*(char *)(param_1 + 0x48) == '\x01') {
      *(undefined *)(param_1 + 0x78) = (&DAT_0075dd14)[*(byte *)(param_1 + 0x60)];
      *(char *)(param_1 + 0x60) = *(char *)(param_1 + 0x60) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x60)) {
        *(undefined1 *)(param_1 + 0x60) = 0;
        *(undefined1 *)(param_1 + 0x48) = 2;
      }
    }
    break;
  case 0xf:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d458)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075dd48)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    break;
  case 0x10:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d490)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1a < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d4c8)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x14 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d4fc)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1a < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    break;
  case 0x11:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d518)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x19 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
  }
  return;
}

