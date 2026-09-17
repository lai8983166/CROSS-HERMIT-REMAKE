
void __fastcall FUN__text__00513480(int param_1)

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
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075cdd0)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1c < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x03') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075ce00)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 6;
      }
    }
  case 2:
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075ce30)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x03') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075ce58)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
        *(undefined1 *)(param_1 + 0x30) = 7;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075ce84)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075ceb8)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075cef8)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x03') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075cf30)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x3f) == '\x03') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075cf58)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075cf90)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075cfcc)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075d008)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d040)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d078)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1a < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d0b0)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075d0e4)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x03') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075d11c)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x03') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075d154)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x03') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075d18c)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 0;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d1c0)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
      }
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d200)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075dbcc)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x21 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0xe;
      }
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d238)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x19 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075dc04)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0xf;
      }
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x3f) == '\x03') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075d270)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x03') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075dc34)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x03') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075dc64)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x1a < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0x10;
      }
    }
    break;
  case 0xc:
    if (*(char *)(param_1 + 0x50) == '\x03') {
      *(undefined *)(param_1 + 0x80) = (&DAT_0075d2a0)[*(byte *)(param_1 + 0x68)];
      *(char *)(param_1 + 0x68) = *(char *)(param_1 + 0x68) + '\x01';
      if (0x1f < *(byte *)(param_1 + 0x68)) {
        *(undefined1 *)(param_1 + 0x68) = 0;
        *(undefined1 *)(param_1 + 0x50) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0x11;
      }
    }
    break;
  case 0xd:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075dc94)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1d < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075dcc8)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0x12;
      }
    }
    break;
  case 0xe:
    if (*(char *)(param_1 + 0x47) == '\x03') {
      *(undefined *)(param_1 + 0x77) = (&DAT_0075dcf8)[*(byte *)(param_1 + 0x5f)];
      *(char *)(param_1 + 0x5f) = *(char *)(param_1 + 0x5f) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x5f)) {
        *(undefined1 *)(param_1 + 0x5f) = 0;
        *(undefined1 *)(param_1 + 0x47) = 0;
      }
    }
    if (*(char *)(param_1 + 0x48) == '\x03') {
      *(undefined *)(param_1 + 0x78) = (&DAT_0075dd28)[*(byte *)(param_1 + 0x60)];
      *(char *)(param_1 + 0x60) = *(char *)(param_1 + 0x60) + '\x01';
      if (0x1e < *(byte *)(param_1 + 0x60)) {
        *(undefined1 *)(param_1 + 0x60) = 0;
        *(undefined1 *)(param_1 + 0x48) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0x13;
      }
    }
    break;
  case 0xf:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d474)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075dd60)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0x14;
      }
    }
    break;
  case 0x10:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d4ac)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d4e0)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075dd80)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0x15;
      }
    }
    break;
  case 0x11:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d534)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0x16;
      }
    }
  }
  return;
}

