
void __fastcall FUN__text__0050afd0(int param_1)

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
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d555)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d5a6)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d618)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d652)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d721)[*(byte *)(param_1 + 0x51)];
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d7aa)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d7fe)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075d806)[*(byte *)(param_1 + 0x55)];
    }
    if (*(char *)(param_1 + 0x3e) == '\x03') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075d84e)[*(byte *)(param_1 + 0x56)];
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d89b)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d8d8)[*(byte *)(param_1 + 0x53)];
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d8f0)[*(byte *)(param_1 + 0x51)];
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d96c)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 0xc:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075c998)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0xc < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075c9c4)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0xd < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075c9f4)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x10 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075ca20)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x12 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075ca4c)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x03') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075ca78)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x25 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x03') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075cab4)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1e < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x03') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075caec)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x10 < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x03') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075cb18)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0xc < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 0;
      }
    }
    if (*(char *)(param_1 + 0x42) == '\x03') {
      *(undefined *)(param_1 + 0x72) = (&DAT_0075cb40)[*(byte *)(param_1 + 0x5a)];
      *(char *)(param_1 + 0x5a) = *(char *)(param_1 + 0x5a) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x5a)) {
        *(undefined1 *)(param_1 + 0x5a) = 0;
        *(undefined1 *)(param_1 + 0x42) = 0;
      }
    }
    if (*(char *)(param_1 + 0x43) == '\x03') {
      *(undefined *)(param_1 + 0x73) = (&DAT_0075cb6c)[*(byte *)(param_1 + 0x5b)];
      *(char *)(param_1 + 0x5b) = *(char *)(param_1 + 0x5b) + '\x01';
      if (0x10 < *(byte *)(param_1 + 0x5b)) {
        *(undefined1 *)(param_1 + 0x5b) = 0;
        *(undefined1 *)(param_1 + 0x43) = 0;
      }
    }
    if (*(char *)(param_1 + 0x44) == '\x03') {
      *(undefined *)(param_1 + 0x74) = (&DAT_0075cb98)[*(byte *)(param_1 + 0x5c)];
      *(char *)(param_1 + 0x5c) = *(char *)(param_1 + 0x5c) + '\x01';
      if (7 < *(byte *)(param_1 + 0x5c)) {
        *(undefined1 *)(param_1 + 0x5c) = 0;
        *(undefined1 *)(param_1 + 0x44) = 0;
      }
    }
    if (*(char *)(param_1 + 0x45) == '\x03') {
      *(undefined *)(param_1 + 0x75) = (&DAT_0075cbb4)[*(byte *)(param_1 + 0x5d)];
      *(char *)(param_1 + 0x5d) = *(char *)(param_1 + 0x5d) + '\x01';
      if (0x28 < *(byte *)(param_1 + 0x5d)) {
        *(undefined1 *)(param_1 + 0x5d) = 0;
        *(undefined1 *)(param_1 + 0x45) = 0;
      }
    }
    if (*(char *)(param_1 + 0x46) == '\x03') {
      *(undefined *)(param_1 + 0x76) = (&DAT_0075cbf4)[*(byte *)(param_1 + 0x5e)];
      *(char *)(param_1 + 0x5e) = *(char *)(param_1 + 0x5e) + '\x01';
      if (0x20 < *(byte *)(param_1 + 0x5e)) {
        *(undefined1 *)(param_1 + 0x5e) = 0;
        *(undefined1 *)(param_1 + 0x46) = 0;
      }
    }
    if (*(char *)(param_1 + 0x47) == '\x03') {
      *(undefined *)(param_1 + 0x77) = (&DAT_0075cc2c)[*(byte *)(param_1 + 0x5f)];
      *(char *)(param_1 + 0x5f) = *(char *)(param_1 + 0x5f) + '\x01';
      if (0x29 < *(byte *)(param_1 + 0x5f)) {
        *(undefined1 *)(param_1 + 0x5f) = 0;
        *(undefined1 *)(param_1 + 0x47) = 0;
      }
    }
    if (*(char *)(param_1 + 0x48) == '\x03') {
      *(undefined *)(param_1 + 0x78) = (&DAT_0075cc6c)[*(byte *)(param_1 + 0x60)];
      *(char *)(param_1 + 0x60) = *(char *)(param_1 + 0x60) + '\x01';
      if (0x10 < *(byte *)(param_1 + 0x60)) {
        *(undefined1 *)(param_1 + 0x60) = 0;
        *(undefined1 *)(param_1 + 0x48) = 0;
      }
    }
    if (*(char *)(param_1 + 0x49) == '\x03') {
      *(undefined *)(param_1 + 0x79) = (&DAT_0075cc94)[*(byte *)(param_1 + 0x61)];
      *(char *)(param_1 + 0x61) = *(char *)(param_1 + 0x61) + '\x01';
      if (0xc < *(byte *)(param_1 + 0x61)) {
        *(undefined1 *)(param_1 + 0x61) = 0;
        *(undefined1 *)(param_1 + 0x49) = 0;
      }
    }
    if (*(char *)(param_1 + 0x4a) == '\x03') {
      *(undefined *)(param_1 + 0x7a) = (&DAT_0075ccb8)[*(byte *)(param_1 + 0x62)];
      *(char *)(param_1 + 0x62) = *(char *)(param_1 + 0x62) + '\x01';
      if (0xc < *(byte *)(param_1 + 0x62)) {
        *(undefined1 *)(param_1 + 0x62) = 0;
        *(undefined1 *)(param_1 + 0x4a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x4b) == '\x03') {
      *(undefined *)(param_1 + 0x7b) = (&DAT_0075ccd8)[*(byte *)(param_1 + 99)];
      *(char *)(param_1 + 99) = *(char *)(param_1 + 99) + '\x01';
      if (0x1f < *(byte *)(param_1 + 99)) {
        *(undefined1 *)(param_1 + 99) = 0;
        *(undefined1 *)(param_1 + 0x4b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x4c) == '\x03') {
      *(undefined *)(param_1 + 0x7c) = (&DAT_0075cd10)[*(byte *)(param_1 + 100)];
      *(char *)(param_1 + 100) = *(char *)(param_1 + 100) + '\x01';
      if (0x16 < *(byte *)(param_1 + 100)) {
        *(undefined1 *)(param_1 + 100) = 0;
        *(undefined1 *)(param_1 + 0x4c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x4d) == '\x03') {
      *(undefined *)(param_1 + 0x7d) = (&DAT_0075cd3c)[*(byte *)(param_1 + 0x65)];
      *(char *)(param_1 + 0x65) = *(char *)(param_1 + 0x65) + '\x01';
      if (0x17 < *(byte *)(param_1 + 0x65)) {
        *(undefined1 *)(param_1 + 0x65) = 0;
        *(undefined1 *)(param_1 + 0x4d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x4e) == '\x03') {
      *(undefined *)(param_1 + 0x7e) = (&DAT_0075cd68)[*(byte *)(param_1 + 0x66)];
      *(char *)(param_1 + 0x66) = *(char *)(param_1 + 0x66) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x66)) {
        *(undefined1 *)(param_1 + 0x66) = 0;
        *(undefined1 *)(param_1 + 0x4e) = 0;
      }
    }
    if (*(char *)(param_1 + 0x4f) == '\x03') {
      *(undefined *)(param_1 + 0x7f) = (&DAT_0075cda0)[*(byte *)(param_1 + 0x67)];
      *(char *)(param_1 + 0x67) = *(char *)(param_1 + 0x67) + '\x01';
      if (0x17 < *(byte *)(param_1 + 0x67)) {
        *(undefined1 *)(param_1 + 0x67) = 0;
        *(undefined1 *)(param_1 + 0x4f) = 0;
      }
    }
  }
  return;
}

