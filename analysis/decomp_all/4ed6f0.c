
void __fastcall FUN__text__004ed6f0(int param_1)

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
      *(undefined *)(param_1 + 0x69) = (&DAT_00756830)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1c < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x03') {
      *(undefined *)(param_1 + 0x71) = (&DAT_00756860)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x32) = 6;
      }
    }
  case 2:
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756890)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x03') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_007568b8)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x11 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
        *(undefined1 *)(param_1 + 0x32) = 7;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_007568e4)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756918)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756958)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3e) == '\x03') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_00756990)[*(byte *)(param_1 + 0x56)];
      *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
      if (0x13 < *(byte *)(param_1 + 0x56)) {
        *(undefined1 *)(param_1 + 0x56) = 0;
        *(undefined1 *)(param_1 + 0x3e) = 0;
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x3f) == '\x03') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_007569b8)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_007569f0)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756a2c)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756a68)[*(byte *)(param_1 + 0x55)];
      *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x55)) {
        *(undefined1 *)(param_1 + 0x55) = 0;
        *(undefined1 *)(param_1 + 0x3d) = 0;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756aa0)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756ad8)[*(byte *)(param_1 + 0x53)];
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
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756b10)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756b44)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3f) == '\x03') {
      *(undefined *)(param_1 + 0x6f) = (&DAT_00756b7c)[*(byte *)(param_1 + 0x57)];
      *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x57)) {
        *(undefined1 *)(param_1 + 0x57) = 0;
        *(undefined1 *)(param_1 + 0x3f) = 0;
      }
    }
    if (*(char *)(param_1 + 0x40) == '\x03') {
      *(undefined *)(param_1 + 0x70) = (&DAT_00756bb4)[*(byte *)(param_1 + 0x58)];
      *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x58)) {
        *(undefined1 *)(param_1 + 0x58) = 0;
        *(undefined1 *)(param_1 + 0x40) = 0;
      }
    }
    if (*(char *)(param_1 + 0x41) == '\x03') {
      *(undefined *)(param_1 + 0x71) = (&DAT_00756bec)[*(byte *)(param_1 + 0x59)];
      *(char *)(param_1 + 0x59) = *(char *)(param_1 + 0x59) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x59)) {
        *(undefined1 *)(param_1 + 0x59) = 0;
        *(undefined1 *)(param_1 + 0x41) = 0;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756c20)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
      }
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_00756c6c)[*(byte *)(param_1 + 0x53)];
      *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
      if (0x18 < *(byte *)(param_1 + 0x53)) {
        *(undefined1 *)(param_1 + 0x53) = 0;
        *(undefined1 *)(param_1 + 0x3b) = 0;
      }
    }
    if (*(char *)(param_1 + 0x3c) == '\x03') {
      *(undefined *)(param_1 + 0x6c) = (&DAT_00756c94)[*(byte *)(param_1 + 0x54)];
      *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
      if (0x15 < *(byte *)(param_1 + 0x54)) {
        *(undefined1 *)(param_1 + 0x54) = 0;
        *(undefined1 *)(param_1 + 0x3c) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x32) = 0xe;
      }
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756cc8)[*(byte *)(param_1 + 0x51)];
      *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x51)) {
        *(undefined1 *)(param_1 + 0x51) = 0;
        *(undefined1 *)(param_1 + 0x39) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x32) = 0x10;
      }
    }
  }
  return;
}

