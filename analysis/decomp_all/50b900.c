
void __fastcall FUN__text__0050b900(int param_1)

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
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d550)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1a < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d56c)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x17 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d584)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x19 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075d5a0)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d5bc)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d608)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d640)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d694)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x39) != '\0') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d6d4)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) != '\0') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d6ec)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3b) != '\0') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d704)[*(byte *)(param_1 + 0x53)];
    }
    if (*(char *)(param_1 + 0x3c) != '\0') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075d720)[*(byte *)(param_1 + 0x54)];
    }
    if (*(char *)(param_1 + 0x3d) != '\0') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075d738)[*(byte *)(param_1 + 0x55)];
    }
    if (*(char *)(param_1 + 0x3e) != '\0') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075d750)[*(byte *)(param_1 + 0x56)];
    }
    if (*(char *)(param_1 + 0x3f) != '\0') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075d768)[*(byte *)(param_1 + 0x57)];
    }
    if (*(char *)(param_1 + 0x40) != '\0') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075d780)[*(byte *)(param_1 + 0x58)];
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d798)[*(byte *)(param_1 + 0x51)];
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d800)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d830)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075d868)[*(byte *)(param_1 + 0x55)];
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075d8a0)[*(byte *)(param_1 + 0x56)];
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d8d8)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d908)[*(byte *)(param_1 + 0x53)];
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d934)[*(byte *)(param_1 + 0x51)];
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075d970)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075d98c)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075d9e4)[*(byte *)(param_1 + 0x53)];
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075da14)[*(byte *)(param_1 + 0x54)];
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075da44)[*(byte *)(param_1 + 0x55)];
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075da74)[*(byte *)(param_1 + 0x56)];
    }
    break;
  case 0xc:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_0075c97c)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075c9a8)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075c9d4)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1d < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_0075ca08)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x17 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075ca34)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075ca60)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x17 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x01') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075caa0)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 2;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x01') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075cad4)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 2;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_0075cb00)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 2;
      }
    }
    if (*(char *)(param_1 + 0x42) == '\x01') {
      *(undefined *)(param_1 + 0x72) = (&DAT_0075cb28)[*(byte *)(param_1 + 0x5a)];
      *(char *)(param_1 + 0x5a) = *(char *)(param_1 + 0x5a) + '\x01';
      if (0x14 < *(byte *)(param_1 + 0x5a)) {
        *(undefined1 *)(param_1 + 0x5a) = 0;
        *(undefined1 *)(param_1 + 0x42) = 2;
      }
    }
    if (*(char *)(param_1 + 0x43) == '\x01') {
      *(undefined *)(param_1 + 0x73) = (&DAT_0075cb54)[*(byte *)(param_1 + 0x5b)];
      *(char *)(param_1 + 0x5b) = *(char *)(param_1 + 0x5b) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x5b)) {
        *(undefined1 *)(param_1 + 0x5b) = 0;
        *(undefined1 *)(param_1 + 0x43) = 2;
      }
    }
    if (*(char *)(param_1 + 0x44) == '\x01') {
      *(undefined *)(param_1 + 0x74) = (&DAT_0075cb80)[*(byte *)(param_1 + 0x5c)];
      *(char *)(param_1 + 0x5c) = *(char *)(param_1 + 0x5c) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x5c)) {
        *(undefined1 *)(param_1 + 0x5c) = 0;
        *(undefined1 *)(param_1 + 0x44) = 2;
      }
    }
    if (*(char *)(param_1 + 0x45) == '\x01') {
      *(undefined *)(param_1 + 0x75) = (&DAT_0075cba0)[*(byte *)(param_1 + 0x5d)];
      *(char *)(param_1 + 0x5d) = *(char *)(param_1 + 0x5d) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x5d)) {
        *(undefined1 *)(param_1 + 0x5d) = 0;
        *(undefined1 *)(param_1 + 0x45) = 2;
      }
    }
    if (*(char *)(param_1 + 0x46) == '\x01') {
      *(undefined *)(param_1 + 0x76) = (&DAT_0075cbe0)[*(byte *)(param_1 + 0x5e)];
      *(char *)(param_1 + 0x5e) = *(char *)(param_1 + 0x5e) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x5e)) {
        *(undefined1 *)(param_1 + 0x5e) = 0;
        *(undefined1 *)(param_1 + 0x46) = 2;
      }
    }
    if (*(char *)(param_1 + 0x47) == '\x01') {
      *(undefined *)(param_1 + 0x77) = (&DAT_0075cc18)[*(byte *)(param_1 + 0x5f)];
      *(char *)(param_1 + 0x5f) = *(char *)(param_1 + 0x5f) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x5f)) {
        *(undefined1 *)(param_1 + 0x5f) = 0;
        *(undefined1 *)(param_1 + 0x47) = 2;
      }
    }
    if (*(char *)(param_1 + 0x48) == '\x01') {
      *(undefined *)(param_1 + 0x78) = (&DAT_0075cc58)[*(byte *)(param_1 + 0x60)];
      *(char *)(param_1 + 0x60) = *(char *)(param_1 + 0x60) + '\x01';
      if (0x12 < *(byte *)(param_1 + 0x60)) {
        *(undefined1 *)(param_1 + 0x60) = 0;
        *(undefined1 *)(param_1 + 0x48) = 2;
      }
    }
    if (*(char *)(param_1 + 0x49) == '\x01') {
      *(undefined *)(param_1 + 0x79) = (&DAT_0075cc80)[*(byte *)(param_1 + 0x61)];
      *(char *)(param_1 + 0x61) = *(char *)(param_1 + 0x61) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x61)) {
        *(undefined1 *)(param_1 + 0x61) = 0;
        *(undefined1 *)(param_1 + 0x49) = 2;
      }
    }
    if (*(char *)(param_1 + 0x4a) == '\x01') {
      *(undefined *)(param_1 + 0x7a) = (&DAT_0075cca4)[*(byte *)(param_1 + 0x62)];
      *(char *)(param_1 + 0x62) = *(char *)(param_1 + 0x62) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x62)) {
        *(undefined1 *)(param_1 + 0x62) = 0;
        *(undefined1 *)(param_1 + 0x4a) = 2;
      }
    }
    if (*(char *)(param_1 + 0x4b) == '\x01') {
      *(undefined *)(param_1 + 0x7b) = (&DAT_0075ccc8)[*(byte *)(param_1 + 99)];
      *(char *)(param_1 + 99) = *(char *)(param_1 + 99) + '\x01';
      if (0xd < *(byte *)(param_1 + 99)) {
        *(undefined1 *)(param_1 + 99) = 0;
        *(undefined1 *)(param_1 + 0x4b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x4c) == '\x01') {
      *(undefined *)(param_1 + 0x7c) = (&DAT_0075ccf8)[*(byte *)(param_1 + 100)];
      *(char *)(param_1 + 100) = *(char *)(param_1 + 100) + '\x01';
      if (0x16 < *(byte *)(param_1 + 100)) {
        *(undefined1 *)(param_1 + 100) = 0;
        *(undefined1 *)(param_1 + 0x4c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x4d) == '\x01') {
      *(undefined *)(param_1 + 0x7d) = (&DAT_0075cd28)[*(byte *)(param_1 + 0x65)];
      *(char *)(param_1 + 0x65) = *(char *)(param_1 + 0x65) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x65)) {
        *(undefined1 *)(param_1 + 0x65) = 0;
        *(undefined1 *)(param_1 + 0x4d) = 2;
      }
    }
    if (*(char *)(param_1 + 0x4e) == '\x01') {
      *(undefined *)(param_1 + 0x7e) = (&DAT_0075cd54)[*(byte *)(param_1 + 0x66)];
      *(char *)(param_1 + 0x66) = *(char *)(param_1 + 0x66) + '\x01';
      if (0x10 < *(byte *)(param_1 + 0x66)) {
        *(undefined1 *)(param_1 + 0x66) = 0;
        *(undefined1 *)(param_1 + 0x4e) = 2;
      }
    }
    if (*(char *)(param_1 + 0x4f) == '\x01') {
      *(undefined *)(param_1 + 0x7f) = (&DAT_0075cd84)[*(byte *)(param_1 + 0x67)];
      *(char *)(param_1 + 0x67) = *(char *)(param_1 + 0x67) + '\x01';
      if (0x19 < *(byte *)(param_1 + 0x67)) {
        *(undefined1 *)(param_1 + 0x67) = 0;
        *(undefined1 *)(param_1 + 0x4f) = 2;
      }
    }
    break;
  case 0xe:
    if (*(char *)(param_1 + 0x45) != '\0') {
      *(undefined *)(param_1 + 0x75) = (&DAT_0075daa0)[*(byte *)(param_1 + 0x5d)];
      *(char *)(param_1 + 0x5d) = *(char *)(param_1 + 0x5d) + '\x01';
      if (0x26 < *(byte *)(param_1 + 0x5d)) {
        *(undefined1 *)(param_1 + 0x5d) = 0;
        *(undefined1 *)(param_1 + 0x45) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3f) != '\0') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_0075dac8)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) != '\0') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075daf8)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x24 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) != '\0') {
      *(undefined *)(param_1 + 0x70) = (&DAT_0075db20)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 0;
      }
    }
    if (*(char *)(param_1 + 0x43) != '\0') {
      *(undefined *)(param_1 + 0x73) = (&DAT_0075db50)[*(byte *)(param_1 + 0x5b)];
      *(char *)(param_1 + 0x5b) = *(char *)(param_1 + 0x5b) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x5b)) {
        *(undefined1 *)(param_1 + 0x5b) = 0;
        *(undefined1 *)(param_1 + 0x43) = 0;
      }
    }
    if (*(char *)(param_1 + 0x44) != '\0') {
      *(undefined *)(param_1 + 0x74) = (&DAT_0075db80)[*(byte *)(param_1 + 0x5c)];
      *(char *)(param_1 + 0x5c) = *(char *)(param_1 + 0x5c) + '\x01';
      if (0x2d < *(byte *)(param_1 + 0x5c)) {
        *(undefined1 *)(param_1 + 0x5c) = 0;
        *(undefined1 *)(param_1 + 0x44) = 0;
      }
    }
  }
  return;
}

