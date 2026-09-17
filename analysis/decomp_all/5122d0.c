
void __fastcall FUN__text__005122d0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0xec) == '\x01') {
    *(ushort *)(param_1 + 0x10e) =
         *(short *)(param_1 + 0x10e) - (ushort)(byte)(&DAT_0075b46c)[*(ushort *)(param_1 + 0xf6)];
    *(short *)(param_1 + 0xf6) = *(short *)(param_1 + 0xf6) + 1;
    if (0x77 < *(ushort *)(param_1 + 0xf6)) {
      *(undefined2 *)(param_1 + 0xf6) = 0;
      *(undefined1 *)(param_1 + 0xec) = 0;
    }
  }
  if (*(char *)(param_1 + 0xed) == '\x01') {
    *(ushort *)(param_1 + 0x110) =
         *(short *)(param_1 + 0x110) +
         (ushort)(byte)(&DAT_0075b4e4)[(uint)*(ushort *)(param_1 + 0xf8) * 2];
    *(ushort *)(param_1 + 0x120) =
         *(short *)(param_1 + 0x120) +
         (ushort)(byte)(&DAT_0075b4e5)[(uint)*(ushort *)(param_1 + 0xf8) * 2];
    *(short *)(param_1 + 0xf8) = *(short *)(param_1 + 0xf8) + 1;
    if (0x6a < *(ushort *)(param_1 + 0xf8)) {
      *(undefined2 *)(param_1 + 0xf8) = 0;
      *(undefined1 *)(param_1 + 0xed) = 0;
    }
  }
  if (*(char *)(param_1 + 0xee) == '\x01') {
    *(ushort *)(param_1 + 0x112) =
         *(short *)(param_1 + 0x112) +
         (ushort)(byte)(&DAT_0075b5bc)[(uint)*(ushort *)(param_1 + 0xfa) * 2];
    *(ushort *)(param_1 + 0x122) =
         *(short *)(param_1 + 0x122) +
         (ushort)(byte)(&DAT_0075b5bd)[(uint)*(ushort *)(param_1 + 0xfa) * 2];
    *(short *)(param_1 + 0xfa) = *(short *)(param_1 + 0xfa) + 1;
    if (0x6a < *(ushort *)(param_1 + 0xfa)) {
      *(undefined2 *)(param_1 + 0xfa) = 0;
      *(undefined1 *)(param_1 + 0xee) = 0;
    }
  }
  if (*(char *)(param_1 + 0xef) == '\x01') {
    *(ushort *)(param_1 + 0x114) =
         *(short *)(param_1 + 0x114) +
         (ushort)(byte)(&DAT_0075b694)[(uint)*(ushort *)(param_1 + 0xfc) * 2];
    *(ushort *)(param_1 + 0x124) =
         *(short *)(param_1 + 0x124) +
         (ushort)(byte)(&DAT_0075b695)[(uint)*(ushort *)(param_1 + 0xfc) * 2];
    *(short *)(param_1 + 0xfc) = *(short *)(param_1 + 0xfc) + 1;
    if (0x6a < *(ushort *)(param_1 + 0xfc)) {
      *(undefined2 *)(param_1 + 0xfc) = 0;
      *(undefined1 *)(param_1 + 0xef) = 0;
    }
  }
  if (*(char *)(param_1 + 0xf0) == '\x01') {
    *(ushort *)(param_1 + 0x116) =
         *(short *)(param_1 + 0x116) +
         (ushort)(byte)(&DAT_0075b76c)[(uint)*(ushort *)(param_1 + 0xfe) * 2];
    *(ushort *)(param_1 + 0x126) =
         *(short *)(param_1 + 0x126) +
         (ushort)(byte)(&DAT_0075b76d)[(uint)*(ushort *)(param_1 + 0xfe) * 2];
    *(short *)(param_1 + 0xfe) = *(short *)(param_1 + 0xfe) + 1;
    if (0x6a < *(ushort *)(param_1 + 0xfe)) {
      *(undefined2 *)(param_1 + 0xfe) = 0;
      *(undefined1 *)(param_1 + 0xf0) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3b) == '\x01') {
    *(undefined2 *)(param_1 + 0xa0) =
         *(undefined2 *)(&DAT_0075b130 + (uint)*(byte *)(param_1 + 0x53) * 2);
    *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
    if (0x6a < *(byte *)(param_1 + 0x53)) {
      *(undefined1 *)(param_1 + 0x53) = 0;
      *(undefined1 *)(param_1 + 0x3b) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3c) == '\x01') {
    *(undefined2 *)(param_1 + 0x88) =
         *(undefined2 *)(&DAT_0075b208 + (uint)*(byte *)(param_1 + 0x54) * 4);
    *(undefined2 *)(param_1 + 0xa2) =
         *(undefined2 *)(&DAT_0075b20a + (uint)*(byte *)(param_1 + 0x54) * 4);
    *(char *)(param_1 + 0x54) = *(char *)(param_1 + 0x54) + '\x01';
    if (0x14 < *(byte *)(param_1 + 0x54)) {
      *(undefined1 *)(param_1 + 0x54) = 0;
      *(undefined1 *)(param_1 + 0x3c) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3d) == '\x01') {
    *(undefined2 *)(param_1 + 0x8a) =
         *(undefined2 *)(&DAT_0075b3b8 + (uint)*(byte *)(param_1 + 0x55) * 2);
    *(char *)(param_1 + 0x55) = *(char *)(param_1 + 0x55) + '\x01';
    if (0x11 < *(byte *)(param_1 + 0x55)) {
      *(undefined1 *)(param_1 + 0x55) = 0;
      *(undefined1 *)(param_1 + 0x3d) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3e) == '\x01') {
    *(undefined2 *)(param_1 + 0x8c) =
         *(undefined2 *)(&DAT_0075b310 + (uint)*(byte *)(param_1 + 0x56) * 4);
    *(undefined2 *)(param_1 + 0xa6) =
         *(undefined2 *)(&DAT_0075b312 + (uint)*(byte *)(param_1 + 0x56) * 4);
    *(char *)(param_1 + 0x56) = *(char *)(param_1 + 0x56) + '\x01';
    if (0x14 < *(byte *)(param_1 + 0x56)) {
      *(undefined1 *)(param_1 + 0x56) = 0;
      *(undefined1 *)(param_1 + 0x3e) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3f) == '\x01') {
    *(undefined2 *)(param_1 + 0x8e) =
         *(undefined2 *)(&DAT_0075b424 + (uint)*(byte *)(param_1 + 0x57) * 2);
    *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
    if (0x11 < *(byte *)(param_1 + 0x57)) {
      *(undefined1 *)(param_1 + 0x57) = 0;
      *(undefined1 *)(param_1 + 0x3f) = 0;
    }
  }
  if (*(char *)(param_1 + 0x40) == '\x01') {
    *(undefined2 *)(param_1 + 0x90) =
         *(undefined2 *)(&DAT_0075b3b8 + (uint)*(byte *)(param_1 + 0x58) * 2);
    *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
    if (0x11 < *(byte *)(param_1 + 0x58)) {
      *(undefined1 *)(param_1 + 0x58) = 0;
      *(undefined1 *)(param_1 + 0x40) = 0;
    }
  }
  return;
}

