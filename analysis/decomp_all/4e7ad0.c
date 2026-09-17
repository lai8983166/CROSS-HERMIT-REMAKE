
void __fastcall FUN__text__004e7ad0(int param_1)

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
  case 2:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756ce4)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1a < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756d00)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x17 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756d18)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x19 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756d34)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756d50)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756d9c)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756dd4)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756e28)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756e68)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756e80)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3b) != '\0') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756e98)[*(byte *)(param_1 + 0x53)];
    }
    if (*(char *)(param_1 + 0x3c) != '\0') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756eb4)[*(byte *)(param_1 + 0x54)];
    }
    if (*(char *)(param_1 + 0x3d) != '\0') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756ecc)[*(byte *)(param_1 + 0x55)];
    }
    if (*(char *)(param_1 + 0x3e) != '\0') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_00756ee4)[*(byte *)(param_1 + 0x56)];
    }
    if (*(char *)(param_1 + 0x3f) != '\0') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_00756efc)[*(byte *)(param_1 + 0x57)];
    }
    if (*(char *)(param_1 + 0x40) != '\0') {
      *(undefined *)(param_1 + 0x70) = (&DAT_00756f14)[*(byte *)(param_1 + 0x58)];
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756f2c)[*(byte *)(param_1 + 0x51)];
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756f94)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756fc4)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756ffc)[*(byte *)(param_1 + 0x55)];
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_00757034)[*(byte *)(param_1 + 0x56)];
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075706c)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075709c)[*(byte *)(param_1 + 0x53)];
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756434)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756434)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756434)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756434)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756434)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_00756434)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 2;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x01') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_00756434)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 2;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x01') {
      *(undefined *)(param_1 + 0x70) = (&DAT_00756434)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 2;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_00756434)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 2;
        *(undefined1 *)(param_1 + 0x40) = 0;
      }
    }
    if (*(char *)(param_1 + 0x42) == '\x01') {
      *(undefined *)(param_1 + 0x72) = (&DAT_00756434)[*(byte *)(param_1 + 0x5a)];
      *(char *)(param_1 + 0x5a) = *(char *)(param_1 + 0x5a) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x5a)) {
        *(undefined1 *)(param_1 + 0x5a) = 0;
        *(undefined1 *)(param_1 + 0x42) = 2;
        *(undefined1 *)(param_1 + 0x41) = 0;
      }
    }
    if (*(char *)(param_1 + 0x43) == '\x01') {
      *(undefined *)(param_1 + 0x73) = (&DAT_00756434)[*(byte *)(param_1 + 0x5b)];
      *(char *)(param_1 + 0x5b) = *(char *)(param_1 + 0x5b) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x5b)) {
        *(undefined1 *)(param_1 + 0x5b) = 0;
        *(undefined1 *)(param_1 + 0x43) = 2;
        *(undefined1 *)(param_1 + 0x42) = 0;
      }
    }
    if (*(char *)(param_1 + 0x44) == '\x01') {
      *(undefined *)(param_1 + 0x74) = (&DAT_00756434)[*(byte *)(param_1 + 0x5c)];
      *(char *)(param_1 + 0x5c) = *(char *)(param_1 + 0x5c) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x5c)) {
        *(undefined1 *)(param_1 + 0x5c) = 0;
        *(undefined1 *)(param_1 + 0x44) = 2;
        *(undefined1 *)(param_1 + 0x43) = 0;
      }
    }
    if (*(char *)(param_1 + 0x45) == '\x01') {
      *(undefined *)(param_1 + 0x75) = (&DAT_00756434)[*(byte *)(param_1 + 0x5d)];
      *(char *)(param_1 + 0x5d) = *(char *)(param_1 + 0x5d) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x5d)) {
        *(undefined1 *)(param_1 + 0x5d) = 0;
        *(undefined1 *)(param_1 + 0x45) = 2;
        *(undefined1 *)(param_1 + 0x44) = 0;
      }
    }
    if (*(char *)(param_1 + 0x46) == '\x01') {
      *(undefined *)(param_1 + 0x76) = (&DAT_00756434)[*(byte *)(param_1 + 0x5e)];
      *(char *)(param_1 + 0x5e) = *(char *)(param_1 + 0x5e) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x5e)) {
        *(undefined1 *)(param_1 + 0x5e) = 0;
        *(undefined1 *)(param_1 + 0x46) = 2;
        *(undefined1 *)(param_1 + 0x45) = 0;
      }
    }
    if (*(char *)(param_1 + 0x47) == '\x01') {
      *(undefined *)(param_1 + 0x77) = (&DAT_00756434)[*(byte *)(param_1 + 0x5f)];
      *(char *)(param_1 + 0x5f) = *(char *)(param_1 + 0x5f) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x5f)) {
        *(undefined1 *)(param_1 + 0x5f) = 0;
        *(undefined1 *)(param_1 + 0x47) = 2;
        *(undefined1 *)(param_1 + 0x46) = 0;
      }
    }
    if (*(char *)(param_1 + 0x48) == '\x01') {
      *(undefined *)(param_1 + 0x78) = (&DAT_00756434)[*(byte *)(param_1 + 0x60)];
      *(char *)(param_1 + 0x60) = *(char *)(param_1 + 0x60) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x60)) {
        *(undefined1 *)(param_1 + 0x60) = 0;
        *(undefined1 *)(param_1 + 0x48) = 2;
        *(undefined1 *)(param_1 + 0x47) = 0;
      }
    }
  }
  return;
}

