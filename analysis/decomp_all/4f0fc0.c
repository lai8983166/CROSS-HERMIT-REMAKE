
void __fastcall FUN__text__004f0fc0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0xea) != '\0') {
    *(ushort *)(param_1 + 0x11a) =
         *(short *)(param_1 + 0x11a) + (ushort)(byte)(&DAT_007550b4)[*(ushort *)(param_1 + 0xf2)];
    *(short *)(param_1 + 0xf2) = *(short *)(param_1 + 0xf2) + 1;
    if (*(short *)(param_1 + 0xf2) == 0x1e) {
      *(undefined1 *)(param_1 + 0xea) = 2;
    }
    if (0x5b < *(ushort *)(param_1 + 0xf2)) {
      *(undefined2 *)(param_1 + 0xf2) = 0;
      *(undefined1 *)(param_1 + 0xea) = 0;
    }
  }
  return;
}

