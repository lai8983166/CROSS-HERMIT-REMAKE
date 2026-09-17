
void __fastcall FUN__text__0051afe0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(*(undefined1 *)(param_1 + 0x37)) {
  case 2:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_0075c488)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x11 < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_0075c4dc)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x1f < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
        *(undefined1 *)(param_1 + 0x37) = 0;
      }
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_0075c51c)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x19 < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
        *(undefined1 *)(param_1 + 0x37) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x30) = 9;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_0075c53c)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x17 < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_0075c5d0)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x14 < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_0075c5e8)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0xc6 < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
      }
    }
    if (*(char *)(param_1 + 299) == '\x03') {
      *(undefined *)(param_1 + 0x12d) = (&DAT_0075c6d4)[*(ushort *)(param_1 + 0x130)];
      *(short *)(param_1 + 0x130) = *(short *)(param_1 + 0x130) + 1;
      if (0x25 < *(ushort *)(param_1 + 0x130)) {
        *(undefined2 *)(param_1 + 0x130) = 0;
        *(undefined1 *)(param_1 + 299) = 0;
        *(undefined1 *)(param_1 + 0x37) = 0;
      }
    }
  }
  return;
}

