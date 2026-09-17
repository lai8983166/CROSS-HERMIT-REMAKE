
void __fastcall FUN__text__004fdd70(int param_1)

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
    *(undefined *)(param_1 + 0x69) = (&DAT_00757940)[*(byte *)(param_1 + 0x51)];
    *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
    if (0x1e < *(byte *)(param_1 + 0x51)) {
      *(undefined1 *)(param_1 + 0x51) = 0;
      *(undefined1 *)(param_1 + 0x39) = 2;
    }
  }
  if (*(char *)(param_1 + 0x3a) == '\x01') {
    *(undefined *)(param_1 + 0x6a) = (&DAT_00757940)[*(byte *)(param_1 + 0x52)];
    *(char *)(param_1 + 0x52) = *(char *)(param_1 + 0x52) + '\x01';
    if (0x1e < *(byte *)(param_1 + 0x52)) {
      *(undefined1 *)(param_1 + 0x52) = 0;
      *(undefined1 *)(param_1 + 0x3a) = 2;
    }
  }
  return;
}

