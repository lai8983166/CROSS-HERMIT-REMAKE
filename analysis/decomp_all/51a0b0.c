
void __fastcall FUN__text__0051a0b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x39) == '\x01') {
    *(ushort *)(param_1 + 0x82) =
         *(short *)(param_1 + 0x82) -
         (ushort)(byte)(&DAT_00759ff8)[(uint)*(byte *)(param_1 + 0x51) * 2];
    *(ushort *)(param_1 + 0x9c) =
         *(short *)(param_1 + 0x9c) -
         (ushort)(byte)(&DAT_00759ff9)[(uint)*(byte *)(param_1 + 0x51) * 2];
    *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
    if (0x16 < *(byte *)(param_1 + 0x51)) {
      *(undefined1 *)(param_1 + 0x51) = 0;
      *(undefined1 *)(param_1 + 0x39) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3a) == '\x01') {
    *(ushort *)(param_1 + 0x84) =
         *(short *)(param_1 + 0x84) -
         (ushort)(byte)(&DAT_0075a028)[(uint)*(byte *)(param_1 + 0x52) * 2];
    *(ushort *)(param_1 + 0x9e) =
         *(short *)(param_1 + 0x9e) +
         (ushort)(byte)(&DAT_0075a029)[(uint)*(byte *)(param_1 + 0x52) * 2];
    *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
    if (0x14 < *(byte *)(param_1 + 0x52)) {
      *(undefined1 *)(param_1 + 0x52) = 0;
      *(undefined1 *)(param_1 + 0x3a) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3b) == '\x01') {
    *(ushort *)(param_1 + 0x86) =
         *(short *)(param_1 + 0x86) +
         (ushort)(byte)(&DAT_0075a054)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(ushort *)(param_1 + 0xa0) =
         *(short *)(param_1 + 0xa0) +
         (ushort)(byte)(&DAT_0075a055)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(ushort *)(param_1 + 0x88) =
         *(short *)(param_1 + 0x88) +
         (ushort)(byte)(&DAT_0075a07c)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(ushort *)(param_1 + 0xa2) =
         *(short *)(param_1 + 0xa2) -
         (ushort)(byte)(&DAT_0075a07d)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(ushort *)(param_1 + 0x8a) =
         *(short *)(param_1 + 0x8a) -
         (ushort)(byte)(&DAT_0075a0a4)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(ushort *)(param_1 + 0xa4) =
         *(short *)(param_1 + 0xa4) +
         (ushort)(byte)(&DAT_0075a0a5)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(ushort *)(param_1 + 0x8c) =
         *(short *)(param_1 + 0x8c) -
         (ushort)(byte)(&DAT_0075a0cc)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(ushort *)(param_1 + 0xa6) =
         *(short *)(param_1 + 0xa6) +
         (ushort)(byte)(&DAT_0075a0cd)[(uint)*(byte *)(param_1 + 0x53) * 2];
    *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
    if (0x13 < *(byte *)(param_1 + 0x53)) {
      *(undefined1 *)(param_1 + 0x53) = 0;
      *(undefined1 *)(param_1 + 0x3b) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3f) == '\x01') {
    *(ushort *)(param_1 + 0x8e) =
         *(short *)(param_1 + 0x8e) +
         (ushort)(byte)(&DAT_0075a0f4)[(uint)*(byte *)(param_1 + 0x57) * 2];
    *(ushort *)(param_1 + 0xa8) =
         *(short *)(param_1 + 0xa8) -
         (ushort)(byte)(&DAT_0075a0f5)[(uint)*(byte *)(param_1 + 0x57) * 2];
    *(char *)(param_1 + 0x57) = *(char *)(param_1 + 0x57) + '\x01';
    if (0x12 < *(byte *)(param_1 + 0x57)) {
      *(undefined1 *)(param_1 + 0x57) = 0;
      *(undefined1 *)(param_1 + 0x3f) = 0;
    }
  }
  if (*(char *)(param_1 + 0x40) == '\x01') {
    *(ushort *)(param_1 + 0x90) =
         *(short *)(param_1 + 0x90) +
         (ushort)(byte)(&DAT_0075a11c)[(uint)*(byte *)(param_1 + 0x58) * 2];
    *(ushort *)(param_1 + 0xaa) =
         *(short *)(param_1 + 0xaa) +
         (ushort)(byte)(&DAT_0075a11d)[(uint)*(byte *)(param_1 + 0x58) * 2];
    *(ushort *)(param_1 + 0x92) =
         *(short *)(param_1 + 0x92) +
         (ushort)(byte)(&DAT_0075a140)[(uint)*(byte *)(param_1 + 0x58) * 2];
    *(ushort *)(param_1 + 0xac) =
         *(short *)(param_1 + 0xac) -
         (ushort)(byte)(&DAT_0075a141)[(uint)*(byte *)(param_1 + 0x58) * 2];
    *(char *)(param_1 + 0x58) = *(char *)(param_1 + 0x58) + '\x01';
    if (0x11 < *(byte *)(param_1 + 0x58)) {
      *(undefined1 *)(param_1 + 0x58) = 0;
      *(undefined1 *)(param_1 + 0x40) = 0;
    }
  }
  if (*(char *)(param_1 + 0x42) == '\x01') {
    *(ushort *)(param_1 + 0x94) =
         *(short *)(param_1 + 0x94) -
         (ushort)(byte)(&DAT_0075a164)[(uint)*(byte *)(param_1 + 0x5a) * 2];
    *(ushort *)(param_1 + 0xae) =
         *(short *)(param_1 + 0xae) -
         (ushort)(byte)(&DAT_0075a165)[(uint)*(byte *)(param_1 + 0x5a) * 2];
    *(char *)(param_1 + 0x5a) = *(char *)(param_1 + 0x5a) + '\x01';
    if (0x10 < *(byte *)(param_1 + 0x5a)) {
      *(undefined1 *)(param_1 + 0x5a) = 0;
      *(undefined1 *)(param_1 + 0x42) = 0;
    }
  }
  if (*(char *)(param_1 + 0x43) == '\x01') {
    *(short *)(param_1 + 0x96) =
         *(short *)(param_1 + 0x96) +
         *(short *)(&DAT_0075a188 + (uint)*(byte *)(param_1 + 0x5b) * 8);
    *(short *)(param_1 + 0xb0) =
         *(short *)(param_1 + 0xb0) +
         *(short *)(&DAT_0075a18a + (uint)*(byte *)(param_1 + 0x5b) * 8);
    *(undefined2 *)(param_1 + 0xca) =
         *(undefined2 *)(&DAT_0075a18c + (uint)*(byte *)(param_1 + 0x5b) * 8);
    *(undefined2 *)(param_1 + 0xe4) =
         *(undefined2 *)(&DAT_0075a18e + (uint)*(byte *)(param_1 + 0x5b) * 8);
    *(char *)(param_1 + 0x5b) = *(char *)(param_1 + 0x5b) + '\x01';
    if (0xf < *(byte *)(param_1 + 0x5b)) {
      *(undefined1 *)(param_1 + 0x5b) = 0;
      *(undefined1 *)(param_1 + 0x43) = 0;
    }
  }
  if (*(char *)(param_1 + 0x44) == '\x01') {
    *(short *)(param_1 + 0x98) =
         *(short *)(param_1 + 0x98) +
         *(short *)(&DAT_0075a230 + (uint)*(byte *)(param_1 + 0x5c) * 8);
    *(short *)(param_1 + 0xb2) =
         *(short *)(param_1 + 0xb2) +
         *(short *)(&DAT_0075a232 + (uint)*(byte *)(param_1 + 0x5c) * 8);
    *(undefined2 *)(param_1 + 0xcc) =
         *(undefined2 *)(&DAT_0075a234 + (uint)*(byte *)(param_1 + 0x5c) * 8);
    *(undefined2 *)(param_1 + 0xe6) =
         *(undefined2 *)(&DAT_0075a236 + (uint)*(byte *)(param_1 + 0x5c) * 8);
    *(char *)(param_1 + 0x5c) = *(char *)(param_1 + 0x5c) + '\x01';
    if (0x10 < *(byte *)(param_1 + 0x5c)) {
      *(undefined1 *)(param_1 + 0x5c) = 0;
      *(undefined1 *)(param_1 + 0x44) = 0;
    }
  }
  if (*(char *)(param_1 + 0x45) == '\x01') {
    *(short *)(param_1 + 0x9a) =
         *(short *)(param_1 + 0x9a) -
         *(short *)(&DAT_0075a2b8 + (uint)*(byte *)(param_1 + 0x5d) * 8);
    *(undefined2 *)(param_1 + 0xce) =
         *(undefined2 *)(&DAT_0075a2bc + (uint)*(byte *)(param_1 + 0x5d) * 8);
    *(undefined2 *)(param_1 + 0xe8) =
         *(undefined2 *)(&DAT_0075a2be + (uint)*(byte *)(param_1 + 0x5d) * 8);
    *(char *)(param_1 + 0x5d) = *(char *)(param_1 + 0x5d) + '\x01';
    if (0x15 < *(byte *)(param_1 + 0x5d)) {
      *(undefined1 *)(param_1 + 0x5d) = 0;
      *(undefined1 *)(param_1 + 0x45) = 0;
    }
  }
  return;
}

