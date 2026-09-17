
void __fastcall FUN__text__004edec0(int param_1)

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
      *(undefined *)(param_1 + 0x69) = (&DAT_00756818)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_00756850)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0xe < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 2;
      }
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_0075687c)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x12 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_007568a4)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x12 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 2;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_007568cc)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x14 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756900)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756934)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x20 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x01') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_0075696c)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x23 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x01') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_007569a4)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 2;
        *(undefined1 *)(param_1 + 0x32) = 8;
        *(undefined1 *)(param_1 + 0x35) = 4;
        *(undefined1 *)(param_1 + 0x34) = 4;
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_007569d4)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756a0c)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x1e < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x01') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756a48)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x1e < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 2;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x3a) == '\x01') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756a84)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756abc)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756af4)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756b2c)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x16 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x01') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_00756b60)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 2;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x01') {
      *(undefined *)(param_1 + 0x70) = (&DAT_00756b98)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 2;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x01') {
      *(undefined *)(param_1 + 0x71) = (&DAT_00756bd0)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 2;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756c08)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756c3c)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x22 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x01') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756c60)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (10 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 2;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x01') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756c88)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (9 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 2;
      }
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x39) == '\x01') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756cac)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x19 < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 2;
      }
    }
  }
  return;
}

