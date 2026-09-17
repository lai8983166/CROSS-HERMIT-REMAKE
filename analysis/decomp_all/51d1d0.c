
void __fastcall FUN__text__0051d1d0(int param_1)

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
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x11a) =
           *(short *)(param_1 + 0x11a) - (ushort)(byte)(&DAT_0075888c)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0x858 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) != '\0') {
      *(ushort *)(param_1 + 0x11c) =
           *(short *)(param_1 + 0x11c) - (ushort)(byte)(&DAT_007590e8)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (0x1e < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    if (*(char *)(param_1 + 0xec) != '\0') {
      *(ushort *)(param_1 + 0x11e) =
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_00759108)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (0x34 < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
      }
    }
    if (*(char *)(param_1 + 0xed) != '\0') {
      *(ushort *)(param_1 + 0x120) =
           *(short *)(param_1 + 0x120) - (ushort)(byte)(&DAT_00759140)[*(ushort *)(param_1 + 0xf8)];
      *(short *)(param_1 + 0xf8) = *(short *)(param_1 + 0xf8) + 1;
      if (0x1e < *(ushort *)(param_1 + 0xf8)) {
        *(undefined2 *)(param_1 + 0xf8) = 0;
        *(undefined1 *)(param_1 + 0xed) = 0;
      }
    }
    if (*(char *)(param_1 + 0xee) != '\0') {
      *(ushort *)(param_1 + 0x122) =
           *(short *)(param_1 + 0x122) - (ushort)(byte)(&DAT_00759160)[*(ushort *)(param_1 + 0xfa)];
      *(short *)(param_1 + 0xfa) = *(short *)(param_1 + 0xfa) + 1;
      if (0x45 < *(ushort *)(param_1 + 0xfa)) {
        *(undefined2 *)(param_1 + 0xfa) = 0;
        *(undefined1 *)(param_1 + 0xee) = 0;
      }
    }
    if (*(char *)(param_1 + 0xef) != '\0') {
      *(ushort *)(param_1 + 0x124) =
           *(short *)(param_1 + 0x124) + (ushort)(byte)(&DAT_007591a8)[*(ushort *)(param_1 + 0xfc)];
      *(short *)(param_1 + 0xfc) = *(short *)(param_1 + 0xfc) + 1;
      if (0x21 < *(ushort *)(param_1 + 0xfc)) {
        *(undefined2 *)(param_1 + 0xfc) = 0;
        *(undefined1 *)(param_1 + 0xef) = 0;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x10a) =
           *(short *)(param_1 + 0x10a) + (ushort)(byte)(&DAT_007591cc)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (*(short *)(param_1 + 0xf2) == 0x24) {
        *(undefined1 *)(param_1 + 0xea) = 2;
        *(undefined1 *)(param_1 + 0xf1) = 0;
      }
      if (*(short *)(param_1 + 0xf2) == 0xb6) {
        *(undefined1 *)(param_1 + 0xea) = 3;
      }
      if (0xca < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) != '\0') {
      *(ushort *)(param_1 + 0x10c) =
           *(short *)(param_1 + 0x10c) + (ushort)(byte)(&DAT_00759298)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (*(short *)(param_1 + 0xf4) == 0x15) {
        *(undefined1 *)(param_1 + 0xeb) = 2;
      }
      if (*(short *)(param_1 + 0xf4) == 0x158) {
        *(undefined1 *)(param_1 + 0xeb) = 3;
      }
      if (0x16b < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0xeb) != '\0') {
      *(ushort *)(param_1 + 0x10c) =
           *(short *)(param_1 + 0x10c) + (ushort)(byte)(&DAT_00759298)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (*(short *)(param_1 + 0xf4) == 0x15) {
        *(undefined1 *)(param_1 + 0xeb) = 2;
      }
      if (*(short *)(param_1 + 0xf4) == 0x158) {
        *(undefined1 *)(param_1 + 0xeb) = 3;
      }
      if (0x16b < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x10a) =
           *(short *)(param_1 + 0x10a) + (ushort)(byte)(&DAT_00759404)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0x69 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
        *(undefined1 *)(param_1 + 0x35) = 0;
      }
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x11a) =
           *(short *)(param_1 + 0x11a) - (ushort)(byte)(&DAT_00759470)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (*(short *)(param_1 + 0xf2) == 0x23) {
        *(undefined1 *)(param_1 + 0xea) = 2;
      }
      if (*(short *)(param_1 + 0xf2) == 0x122) {
        *(undefined1 *)(param_1 + 0xea) = 3;
      }
      if (0x160 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) != '\0') {
      *(ushort *)(param_1 + 0x11c) =
           *(short *)(param_1 + 0x11c) - (ushort)(byte)(&DAT_007595d4)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (*(short *)(param_1 + 0xf4) == 0x23) {
        *(undefined1 *)(param_1 + 0xeb) = 2;
      }
      if (*(short *)(param_1 + 0xf4) == 0x127) {
        *(undefined1 *)(param_1 + 0xeb) = 3;
      }
      if (0x164 < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    if (*(char *)(param_1 + 0xec) != '\0') {
      *(ushort *)(param_1 + 0x11e) =
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_0075973c)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (*(short *)(param_1 + 0xf6) == 0x23) {
        *(undefined1 *)(param_1 + 0xec) = 2;
      }
      if (*(short *)(param_1 + 0xf6) == 300) {
        *(undefined1 *)(param_1 + 0xec) = 3;
      }
      if (0x168 < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
        *(undefined1 *)(param_1 + 0x35) = 6;
        *(undefined1 *)(param_1 + 0x30) = 0xb;
      }
    }
    if (*(char *)(param_1 + 0xed) != '\0') {
      *(ushort *)(param_1 + 0x120) =
           *(short *)(param_1 + 0x120) + (ushort)(byte)(&DAT_007598a8)[*(ushort *)(param_1 + 0xf8)];
      *(short *)(param_1 + 0xf8) = *(short *)(param_1 + 0xf8) + 1;
      if (*(short *)(param_1 + 0xf8) == 0x96) {
        *(undefined1 *)(param_1 + 0xed) = 3;
      }
      if (0xd1 < *(ushort *)(param_1 + 0xf8)) {
        *(undefined2 *)(param_1 + 0xf8) = 0;
        *(undefined1 *)(param_1 + 0xed) = 0;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0xed) != '\0') {
      *(ushort *)(param_1 + 0x120) =
           *(short *)(param_1 + 0x120) + (ushort)(byte)(&DAT_007598a8)[*(ushort *)(param_1 + 0xf8)];
      *(short *)(param_1 + 0xf8) = *(short *)(param_1 + 0xf8) + 1;
      if (*(short *)(param_1 + 0xf8) == 0x96) {
        *(undefined1 *)(param_1 + 0xed) = 3;
      }
      if (0xd1 < *(ushort *)(param_1 + 0xf8)) {
        *(undefined2 *)(param_1 + 0xf8) = 0;
        *(undefined1 *)(param_1 + 0xed) = 0;
      }
    }
    if (*(char *)(param_1 + 0xec) != '\0') {
      *(ushort *)(param_1 + 0x11e) =
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_0075997c)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (*(short *)(param_1 + 0xf6) == 0x1b) {
        *(undefined1 *)(param_1 + 0xec) = 2;
      }
      if (*(short *)(param_1 + 0xf6) == 0xaf) {
        *(undefined1 *)(param_1 + 0xec) = 3;
      }
      if (0xc9 < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0xec) != '\0') {
      *(ushort *)(param_1 + 0x11e) =
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_0075997c)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (*(short *)(param_1 + 0xf6) == 0x1b) {
        *(undefined1 *)(param_1 + 0xec) = 2;
      }
      if (*(short *)(param_1 + 0xf6) == 0xaf) {
        *(undefined1 *)(param_1 + 0xec) = 3;
      }
      if (0xc9 < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
        *(undefined1 *)(param_1 + 0x35) = 0;
        *(undefined1 *)(param_1 + 0x30) = 0xd;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x10a) =
           *(short *)(param_1 + 0x10a) - (ushort)(byte)(&DAT_00759a48)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (*(short *)(param_1 + 0xf2) == 0x2b) {
        *(undefined1 *)(param_1 + 0xea) = 2;
      }
      if (*(short *)(param_1 + 0xf2) == 0x92) {
        *(undefined1 *)(param_1 + 0xea) = 3;
      }
      if (0xb1 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
        *(undefined1 *)(param_1 + 0x35) = 0;
      }
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x10a) =
           *(short *)(param_1 + 0x10a) + (ushort)(byte)(&DAT_00759afc)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (*(short *)(param_1 + 0xf2) == 0x1c) {
        *(undefined1 *)(param_1 + 0xea) = 2;
      }
      if (0x82 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) != '\0') {
      *(ushort *)(param_1 + 0x11c) =
           *(short *)(param_1 + 0x11c) + (ushort)(byte)(&DAT_00759b80)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (*(short *)(param_1 + 0xf4) == 0x1c) {
        *(undefined1 *)(param_1 + 0xeb) = 2;
      }
      if (0x70 < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    if (*(char *)(param_1 + 0xec) != '\0') {
      *(ushort *)(param_1 + 0x11e) =
           *(short *)(param_1 + 0x11e) + (ushort)(byte)(&DAT_00759bf4)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (*(short *)(param_1 + 0xf6) == 0x23) {
        *(undefined1 *)(param_1 + 0xec) = 2;
      }
      if (*(short *)(param_1 + 0xf6) == 0x6a) {
        *(undefined1 *)(param_1 + 0xec) = 3;
      }
      if (0x93 < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
        *(undefined1 *)(param_1 + 0x35) = 0;
      }
    }
    if (*(char *)(param_1 + 0xed) != '\0') {
      *(ushort *)(param_1 + 0x110) =
           *(short *)(param_1 + 0x110) + (ushort)(byte)(&DAT_00759c88)[*(ushort *)(param_1 + 0xf8)];
      *(short *)(param_1 + 0xf8) = *(short *)(param_1 + 0xf8) + 1;
      if (*(short *)(param_1 + 0xf8) == 0x23) {
        *(undefined1 *)(param_1 + 0xed) = 2;
      }
      if (*(short *)(param_1 + 0xf8) == 0x65) {
        *(undefined1 *)(param_1 + 0xed) = 3;
      }
      if (0x85 < *(ushort *)(param_1 + 0xf8)) {
        *(undefined2 *)(param_1 + 0xf8) = 0;
        *(undefined1 *)(param_1 + 0xed) = 0;
      }
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x11a) =
           *(short *)(param_1 + 0x11a) + (ushort)(byte)(&DAT_00759d10)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0xcf < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
        *(undefined1 *)(param_1 + 0x35) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) != '\0') {
      *(ushort *)(param_1 + 0x11c) =
           *(short *)(param_1 + 0x11c) - (ushort)(byte)(&DAT_00759de0)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (*(short *)(param_1 + 0xf4) == 0x3f) {
        *(undefined1 *)(param_1 + 0xeb) = 3;
      }
      if (0x66 < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    if (*(char *)(param_1 + 0xec) != '\0') {
      *(ushort *)(param_1 + 0x11e) =
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_00759e48)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (*(short *)(param_1 + 0xf6) == 0x27) {
        *(undefined1 *)(param_1 + 0xec) = 2;
      }
      if (*(short *)(param_1 + 0xf6) == 0x56) {
        *(undefined1 *)(param_1 + 0xec) = 3;
      }
      if (0x7b < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
      }
    }
    break;
  case 0xc:
    if (*(char *)(param_1 + 0xea) != '\0') {
      *(ushort *)(param_1 + 0x11a) =
           *(short *)(param_1 + 0x11a) + (ushort)(byte)(&DAT_00759ec4)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0x132 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
        *(undefined1 *)(param_1 + 0x35) = 0;
      }
    }
  }
  return;
}

