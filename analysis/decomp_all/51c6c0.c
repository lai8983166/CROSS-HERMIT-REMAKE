
void __fastcall FUN__text__0051c6c0(int param_1)

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
      *(undefined *)(param_1 + 0x105) = (&DAT_0075becc)[*(ushort *)(param_1 + 0xf8)];
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0xea) == '\x03') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075bf4e)[*(ushort *)(param_1 + 0xf2)];
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0xeb) == '\x03') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075bedc)[*(ushort *)(param_1 + 0xf4)];
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0xea) == '\x03') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075bf4a)[*(ushort *)(param_1 + 0xf2)];
    }
    if (*(char *)(param_1 + 0xeb) == '\x03') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075bfa9)[*(ushort *)(param_1 + 0xf4)];
    }
    if (*(char *)(param_1 + 0xec) == '\x03') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c008)[*(ushort *)(param_1 + 0xf6)];
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0xed) == '\x03') {
      *(undefined *)(param_1 + 0x105) = (&DAT_0075c0de)[*(ushort *)(param_1 + 0xf8)];
    }
    if (*(char *)(param_1 + 0xeb) == '\x03') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075c264)[*(ushort *)(param_1 + 0xf4)];
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
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c1ed)[*(ushort *)(param_1 + 0xf6)];
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0xea) == '\x03') {
      *(undefined *)(param_1 + 0x102) = (&DAT_0075c252)[*(ushort *)(param_1 + 0xf2)];
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0xec) == '\x03') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c2f6)[*(ushort *)(param_1 + 0xf6)];
    }
    if (*(char *)(param_1 + 0xed) == '\x03') {
      *(undefined *)(param_1 + 0x105) = (&DAT_0075c34b)[*(ushort *)(param_1 + 0xf8)];
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0xeb) == '\x03') {
      *(undefined *)(param_1 + 0x103) = (&DAT_0075c395)[*(ushort *)(param_1 + 0xf4)];
    }
    if (*(char *)(param_1 + 0xec) == '\x03') {
      *(undefined *)(param_1 + 0x104) = (&DAT_0075c3ce)[*(ushort *)(param_1 + 0xf6)];
    }
  }
  return;
}

