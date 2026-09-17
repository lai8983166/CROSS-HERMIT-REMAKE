
void __fastcall FUN__text__0051ca00(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(*(undefined1 *)(param_1 + 0x35)) {
  case 1:
    if ((*(char *)(param_1 + 0xea) == '\x01') &&
       (*(undefined *)(param_1 + 0x102) = (&DAT_0075be74)[*(ushort *)(param_1 + 0xf2)],
       *(short *)(param_1 + 0xf2) == 0x56)) {
      *(undefined1 *)(param_1 + 0xea) = 2;
    }
    if ((*(char *)(param_1 + 0xee) == '\x01') &&
       (*(undefined *)(param_1 + 0x106) = (&DAT_0075beec)[*(ushort *)(param_1 + 0xfa)],
       *(short *)(param_1 + 0xfa) == 0x19)) {
      *(undefined1 *)(param_1 + 0xee) = 2;
    }
    if ((*(char *)(param_1 + 0xef) == '\x01') &&
       (*(undefined *)(param_1 + 0x107) = (&DAT_0075bf08)[*(ushort *)(param_1 + 0xfc)],
       *(short *)(param_1 + 0xfc) == 10)) {
      *(undefined1 *)(param_1 + 0xef) = 2;
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0xea) == '\x01') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075bf14)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0x1a < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) == '\x01') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075bf30)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (0x1a < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    if (*(char *)(param_1 + 0xec) == '\x01') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075bf4c)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (0x18 < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
      }
    }
    if (*(char *)(param_1 + 0xed) == '\x01') {
      *(undefined *)(param_1 + 0x105) = (&DAT_0075bf68)[*(ushort *)(param_1 + 0xf8)];
      *(short *)(param_1 + 0xf8) = *(short *)(param_1 + 0xf8) + 1;
      if (0x1b < *(ushort *)(param_1 + 0xf8)) {
        *(undefined2 *)(param_1 + 0xf8) = 0;
        *(undefined1 *)(param_1 + 0xed) = 0;
      }
    }
    if (*(char *)(param_1 + 0xee) == '\x01') {
      *(undefined *)(param_1 + 0x106) = (&DAT_0075bf84)[*(ushort *)(param_1 + 0xfa)];
      *(short *)(param_1 + 0xfa) = *(short *)(param_1 + 0xfa) + 1;
      if (0x18 < *(ushort *)(param_1 + 0xfa)) {
        *(undefined2 *)(param_1 + 0xfa) = 0;
        *(undefined1 *)(param_1 + 0xee) = 0;
      }
    }
    if (*(char *)(param_1 + 0xef) == '\x01') {
      *(undefined *)(param_1 + 0x107) = (&DAT_0075bfa0)[*(ushort *)(param_1 + 0xfc)];
      *(short *)(param_1 + 0xfc) = *(short *)(param_1 + 0xfc) + 1;
      if (0x18 < *(ushort *)(param_1 + 0xfc)) {
        *(undefined2 *)(param_1 + 0xfc) = 0;
        *(undefined1 *)(param_1 + 0xef) = 0;
      }
    }
    if (*(char *)(param_1 + 0xf0) == '\x01') {
      *(undefined *)(param_1 + 0x108) = (&DAT_0075bfbc)[*(ushort *)(param_1 + 0xfe)];
      *(short *)(param_1 + 0xfe) = *(short *)(param_1 + 0xfe) + 1;
      if (0x18 < *(ushort *)(param_1 + 0xfe)) {
        *(undefined2 *)(param_1 + 0xfe) = 0;
        *(undefined1 *)(param_1 + 0xf0) = 0;
      }
    }
    if (*(char *)(param_1 + 0xf1) == '\x01') {
      *(undefined *)(param_1 + 0x109) = (&DAT_0075bfd8)[*(ushort *)(param_1 + 0x100)];
      *(short *)(param_1 + 0x100) = *(short *)(param_1 + 0x100) + 1;
      if (2 < *(ushort *)(param_1 + 0x100)) {
        *(undefined2 *)(param_1 + 0x100) = 0;
        *(undefined1 *)(param_1 + 0xf1) = 2;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0xea) == '\x01') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075bfdc)[*(ushort *)(param_1 + 0xf2)];
    }
    if (*(char *)(param_1 + 0xeb) == '\x01') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075c01c)[*(ushort *)(param_1 + 0xf4)];
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0xea) == '\x01') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075c048)[*(ushort *)(param_1 + 0xf2)];
    }
    if (*(char *)(param_1 + 0xeb) == '\x01') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075c0ac)[*(ushort *)(param_1 + 0xf4)];
    }
    if (*(char *)(param_1 + 0xec) == '\x01') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c110)[*(ushort *)(param_1 + 0xf6)];
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0xea) == '\x01') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075c1b0)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0x76 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) == '\x01') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075c228)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (0x3b < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 2;
      }
    }
    if (*(char *)(param_1 + 0xec) == '\x01') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c280)[*(ushort *)(param_1 + 0xf6)];
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0xec) == '\x01') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c280)[*(ushort *)(param_1 + 0xf6)];
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0xea) == '\x01') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075c2b8)[*(ushort *)(param_1 + 0xf2)];
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0xea) == '\x01') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075c304)[*(ushort *)(param_1 + 0xf2)];
    }
    if (*(char *)(param_1 + 0xeb) == '\x01') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075c320)[*(ushort *)(param_1 + 0xf4)];
    }
    if (*(char *)(param_1 + 0xec) == '\x01') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c33c)[*(ushort *)(param_1 + 0xf6)];
    }
    if (*(char *)(param_1 + 0xed) == '\x01') {
      *(undefined *)(param_1 + 0x105) = (&DAT_0075c38c)[*(ushort *)(param_1 + 0xf8)];
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0xec) == '\x01') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c3fc)[*(ushort *)(param_1 + 0xf6)];
    }
  }
  return;
}

