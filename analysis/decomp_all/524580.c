
void __fastcall FUN__text__00524580(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x39) == '\x03') {
    *(undefined *)(param_1 + 0x69) = (&DAT_0075bb9c)[*(byte *)(param_1 + 0x51)];
    *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
    if (0x29 < *(byte *)(param_1 + 0x51)) {
      *(undefined1 *)(param_1 + 0x51) = 0;
      *(undefined1 *)(param_1 + 0x39) = 0;
      *(undefined1 *)(param_1 + 0x30) = 1;
    }
  }
  if (*(char *)(param_1 + 0x3a) == '\x03') {
    *(undefined *)(param_1 + 0x6a) = (&DAT_0075bbdc)[*(byte *)(param_1 + 0x52)];
    *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
    if (0x16 < *(byte *)(param_1 + 0x52)) {
      *(undefined1 *)(param_1 + 0x52) = 0;
      *(undefined1 *)(param_1 + 0x3a) = 0;
    }
  }
  if (*(char *)(param_1 + 0x3b) == '\x03') {
    *(undefined *)(param_1 + 0x6b) = (&DAT_0075bc08)[*(byte *)(param_1 + 0x53)];
    *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
    if (0x13 < *(byte *)(param_1 + 0x53)) {
      *(undefined1 *)(param_1 + 0x53) = 0;
      *(undefined1 *)(param_1 + 0x3b) = 0;
    }
  }
  return;
}

