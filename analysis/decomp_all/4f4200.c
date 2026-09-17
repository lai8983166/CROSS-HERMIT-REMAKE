
void __fastcall FUN__text__004f4200(int param_1)

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
           *(short *)(param_1 + 0x11a) - (ushort)(byte)(&DAT_00753298)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0x858 < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
      }
    }
    if (*(char *)(param_1 + 0xeb) != '\0') {
      *(ushort *)(param_1 + 0x11c) =
           *(short *)(param_1 + 0x11c) - (ushort)(byte)(&DAT_00753af4)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (0x1e < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
      }
    }
    if (*(char *)(param_1 + 0xec) != '\0') {
      *(ushort *)(param_1 + 0x11e) =
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_00753b14)[*(ushort *)(param_1 + 0xf6)];
      *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
      if (0x34 < *(ushort *)(param_1 + 0xf6)) {
        *(undefined2 *)(param_1 + 0xf6) = 0;
        *(undefined1 *)(param_1 + 0xec) = 0;
      }
    }
    if (*(char *)(param_1 + 0xed) != '\0') {
      *(ushort *)(param_1 + 0x120) =
           *(short *)(param_1 + 0x120) - (ushort)(byte)(&DAT_00753b4c)[*(ushort *)(param_1 + 0xf8)];
      *(short *)(param_1 + 0xf8) = *(short *)(param_1 + 0xf8) + 1;
      if (0x1e < *(ushort *)(param_1 + 0xf8)) {
        *(undefined2 *)(param_1 + 0xf8) = 0;
        *(undefined1 *)(param_1 + 0xed) = 0;
      }
    }
    if (*(char *)(param_1 + 0xee) != '\0') {
      *(ushort *)(param_1 + 0x122) =
           *(short *)(param_1 + 0x122) - (ushort)(byte)(&DAT_00753b6c)[*(ushort *)(param_1 + 0xfa)];
      *(short *)(param_1 + 0xfa) = *(short *)(param_1 + 0xfa) + 1;
      if (0x45 < *(ushort *)(param_1 + 0xfa)) {
        *(undefined2 *)(param_1 + 0xfa) = 0;
        *(undefined1 *)(param_1 + 0xee) = 0;
      }
    }
    if (*(char *)(param_1 + 0xef) != '\0') {
      *(ushort *)(param_1 + 0x124) =
           *(short *)(param_1 + 0x124) + (ushort)(byte)(&DAT_00753bb4)[*(ushort *)(param_1 + 0xfc)];
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
           *(short *)(param_1 + 0x10a) + (ushort)(byte)(&DAT_00753bd8)[*(ushort *)(param_1 + 0xf2)];
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
           *(short *)(param_1 + 0x10c) + (ushort)(byte)(&DAT_00753ca4)[*(ushort *)(param_1 + 0xf4)];
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
           *(short *)(param_1 + 0x10c) + (ushort)(byte)(&DAT_00753ca4)[*(ushort *)(param_1 + 0xf4)];
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
           *(short *)(param_1 + 0x10a) + (ushort)(byte)(&DAT_00753e10)[*(ushort *)(param_1 + 0xf2)];
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
           *(short *)(param_1 + 0x11a) - (ushort)(byte)(&DAT_00753e7c)[*(ushort *)(param_1 + 0xf2)];
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
           *(short *)(param_1 + 0x11c) - (ushort)(byte)(&DAT_00753fe0)[*(ushort *)(param_1 + 0xf4)];
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
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_00754148)[*(ushort *)(param_1 + 0xf6)];
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
        *(undefined1 *)(param_1 + 0x32) = 0xb;
      }
    }
    if (*(char *)(param_1 + 0xed) != '\0') {
      *(ushort *)(param_1 + 0x120) =
           *(short *)(param_1 + 0x120) + (ushort)(byte)(&DAT_007542b4)[*(ushort *)(param_1 + 0xf8)];
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
           *(short *)(param_1 + 0x120) + (ushort)(byte)(&DAT_007542b4)[*(ushort *)(param_1 + 0xf8)];
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
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_00754388)[*(ushort *)(param_1 + 0xf6)];
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
           *(short *)(param_1 + 0x11e) - (ushort)(byte)(&DAT_00754388)[*(ushort *)(param_1 + 0xf6)];
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
        *(undefined1 *)(param_1 + 0x32) = 0xd;
      }
    }
  }
  return;
}

