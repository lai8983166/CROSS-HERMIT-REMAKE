
void __fastcall FUN__text__004f2640(int param_1)

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
      *(undefined *)(param_1 + 300) = (&DAT_007564a8)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x11 < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_007564fc)[*(ushort *)(param_1 + 0x12e)];
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
      *(undefined *)(param_1 + 300) = (&DAT_0075653c)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x19 < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
        *(undefined1 *)(param_1 + 0x37) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x32) = 9;
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x12a) == '\x03') {
      *(undefined *)(param_1 + 300) = (&DAT_00756568)[*(ushort *)(param_1 + 0x12e)];
      *(short *)(param_1 + 0x12e) = *(short *)(param_1 + 0x12e) + 1;
      if (0x2e < *(ushort *)(param_1 + 0x12e)) {
        *(undefined2 *)(param_1 + 0x12e) = 0;
        *(undefined1 *)(param_1 + 0x12a) = 0;
        *(undefined1 *)(param_1 + 0x37) = 0;
      }
    }
  }
  return;
}

