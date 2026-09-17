
void __fastcall FUN__text__004f1440(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x36) != '\0') {
    *(undefined2 *)(param_1 + 0xb6) =
         *(undefined2 *)(&DAT_00756598 + (uint)*(byte *)(param_1 + 0x51) * 6);
    *(undefined2 *)(param_1 + 0xd0) =
         *(undefined2 *)(&DAT_0075659a + (uint)*(byte *)(param_1 + 0x51) * 6);
    *(char *)(param_1 + 0x51) = *(char *)(param_1 + 0x51) + '\x01';
    if (*(char *)(param_1 + 0x51) == '\x1f') {
      *(undefined1 *)(param_1 + 0x36) = 2;
    }
    if (*(char *)(param_1 + 0x51) == 'B') {
      *(undefined1 *)(param_1 + 0x36) = 3;
    }
    if (100 < *(byte *)(param_1 + 0x51)) {
      *(undefined1 *)(param_1 + 0x51) = 0;
      *(undefined1 *)(param_1 + 0x36) = 0;
      *(undefined1 *)(param_1 + 0x32) = 4;
    }
  }
  return;
}

