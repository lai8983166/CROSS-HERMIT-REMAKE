
void __fastcall FUN__text__004f3810(int param_1)

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
    if (*(char *)(param_1 + 0xed) == '\x01') {
      *(undefined *)(param_1 + 0x105) = (&DAT_00756048)[*(ushort *)(param_1 + 0xf8)];
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0xea) == '\x03') {
      *(undefined *)(param_1 + 0x102) = (&DAT_007560ca)[*(ushort *)(param_1 + 0xf2)];
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0xeb) == '\x03') {
      *(undefined *)(param_1 + 0x103) = (&DAT_00756058)[*(ushort *)(param_1 + 0xf4)];
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0xea) == '\x03') {
      *(undefined *)(param_1 + 0x102) = (&DAT_007560c6)[*(ushort *)(param_1 + 0xf2)];
    }
    if (*(char *)(param_1 + 0xeb) == '\x03') {
      *(undefined *)(param_1 + 0x103) = (&DAT_00756125)[*(ushort *)(param_1 + 0xf4)];
    }
    if (*(char *)(param_1 + 0xec) == '\x03') {
      *(undefined *)(param_1 + 0x104) = (&DAT_00756184)[*(ushort *)(param_1 + 0xf6)];
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0xed) == '\x03') {
      *(undefined *)(param_1 + 0x105) = (&DAT_0075625a)[*(ushort *)(param_1 + 0xf8)];
    }
    if (*(char *)(param_1 + 0xeb) == '\x03') {
      *(undefined *)(param_1 + 0x103) = (&DAT_007563e0)[*(ushort *)(param_1 + 0xf4)];
      *(short *)(param_1 + 0xf4) = *(short *)(param_1 + 0xf4) + 1;
      if (0x1a < *(ushort *)(param_1 + 0xf4)) {
        *(undefined2 *)(param_1 + 0xf4) = 0;
        *(undefined1 *)(param_1 + 0xeb) = 0;
        *(undefined1 *)(param_1 + 0x35) = 7;
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0xec) == '\x03') {
      *(undefined *)(param_1 + 0x104) = (&DAT_00756369)[*(ushort *)(param_1 + 0xf6)];
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0xea) == '\x03') {
      *(undefined *)(param_1 + 0x102) = (&DAT_00756450)[*(ushort *)(param_1 + 0xf2)];
      *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
      if (0x1b < *(ushort *)(param_1 + 0xf2)) {
        *(undefined2 *)(param_1 + 0xf2) = 0;
        *(undefined1 *)(param_1 + 0xea) = 0;
        *(undefined1 *)(param_1 + 0x35) = 0;
        *(undefined1 *)(param_1 + 0x32) = 0x11;
      }
    }
  }
  return;
}

