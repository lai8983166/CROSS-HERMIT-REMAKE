
void __fastcall FUN__text__004fdae0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0xea) == '\x01') {
    *(undefined *)(param_1 + 0x102) = (&DAT_00757980)[*(ushort *)(param_1 + 0xf2)];
    *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
    if (0x1e < *(ushort *)(param_1 + 0xf2)) {
      *(undefined2 *)(param_1 + 0xf2) = 0;
      *(undefined1 *)(param_1 + 0xea) = 2;
    }
  }
  return;
}

