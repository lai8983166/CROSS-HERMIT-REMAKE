
void __fastcall FUN__text__0051b8b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(char *)(param_1 + 0x37) == '\x03') && (*(char *)(param_1 + 0x12a) != '\0')) {
    *(ushort *)(param_1 + 0x134) =
         *(short *)(param_1 + 0x134) - (ushort)(byte)(&DAT_0075b844)[*(ushort *)(param_1 + 0x130)];
    *(ushort *)(param_1 + 0x13a) =
         *(short *)(param_1 + 0x13a) - (ushort)(byte)(&DAT_0075b844)[*(ushort *)(param_1 + 0x130)];
    *(ushort *)(param_1 + 0x13c) =
         *(short *)(param_1 + 0x13c) + (ushort)(byte)(&DAT_0075b844)[*(ushort *)(param_1 + 0x130)];
    *(short *)(param_1 + 0x130) = *(short *)(param_1 + 0x130) + 1;
    if (0x1ad < *(ushort *)(param_1 + 0x130)) {
      *(undefined2 *)(param_1 + 0x130) = 0;
      *(undefined1 *)(param_1 + 299) = 0;
    }
  }
  return;
}

