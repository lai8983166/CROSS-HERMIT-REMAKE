
void __fastcall FUN__text__004e7830(int param_1)

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
  case 3:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756ce9)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756d3a)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756dac)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756de6)[*(byte *)(param_1 + 0x52)];
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756eb5)[*(byte *)(param_1 + 0x51)];
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x39) == '\x03') {
      *(undefined *)(param_1 + 0x69) = (&DAT_00756f3e)[*(byte *)(param_1 + 0x51)];
    }
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_00756f92)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3d) == '\x03') {
      *(undefined *)(param_1 + 0x6d) = (&DAT_00756f9a)[*(byte *)(param_1 + 0x55)];
    }
    if (*(char *)(param_1 + 0x3e) == '\x03') {
      *(undefined *)(param_1 + 0x6e) = (&DAT_00756fe2)[*(byte *)(param_1 + 0x56)];
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_0075702f)[*(byte *)(param_1 + 0x52)];
    }
    if (*(char *)(param_1 + 0x3b) == '\x03') {
      *(undefined *)(param_1 + 0x6b) = (&DAT_0075706c)[*(byte *)(param_1 + 0x53)];
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0x3a) == '\x03') {
      *(undefined *)(param_1 + 0x6a) = (&DAT_007570c8)[*(byte *)(param_1 + 0x52)];
      *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
      if (0x20 < *(byte *)(param_1 + 0x52)) {
        *(undefined1 *)(param_1 + 0x52) = 0;
        *(undefined1 *)(param_1 + 0x3a) = 0;
      }
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0x48) == '\x03') {
      *(undefined *)(param_1 + 0x78) = (&DAT_00756450)[*(byte *)(param_1 + 0x60)];
      *(char *)(param_1 + 0x60) = *(char *)(param_1 + 0x60) + '\x01';
      if (0x1b < *(byte *)(param_1 + 0x60)) {
        *(undefined1 *)(param_1 + 0x60) = 0;
        *(undefined1 *)(param_1 + 0x48) = 0;
        *(undefined1 *)(param_1 + 0x34) = 0;
        *(undefined1 *)(param_1 + 0x32) = 0xf;
      }
    }
  }
  return;
}

