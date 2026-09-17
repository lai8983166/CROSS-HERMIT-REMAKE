
void __fastcall FUN__text__005246a0(int param_1)

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
    *(undefined *)(param_1 + 0x69) = (&DAT_0075bb84)[*(byte *)(param_1 + 0x51)];
    *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
    if (0x16 < *(byte *)(param_1 + 0x51)) {
      *(undefined1 *)(param_1 + 0x51) = 0;
      *(undefined1 *)(param_1 + 0x39) = 2;
    }
  }
  if (*(char *)(param_1 + 0x3a) == '\x01') {
    *(undefined *)(param_1 + 0x6a) = (&DAT_0075bbc8)[*(byte *)(param_1 + 0x52)];
    *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
    if (0x11 < *(byte *)(param_1 + 0x52)) {
      *(undefined1 *)(param_1 + 0x52) = 0;
      *(undefined1 *)(param_1 + 0x3a) = 2;
    }
  }
  if (*(char *)(param_1 + 0x3b) == '\x01') {
    *(undefined *)(param_1 + 0x6b) = (&DAT_0075bbf4)[*(byte *)(param_1 + 0x53)];
    *(char *)(param_1 + 0x53) = *(char *)(param_1 + 0x53) + '\x01';
    if (0x11 < *(byte *)(param_1 + 0x53)) {
      *(undefined1 *)(param_1 + 0x53) = 0;
      *(undefined1 *)(param_1 + 0x3b) = 2;
    }
  }
  return;
}

