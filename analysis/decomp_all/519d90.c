
void __fastcall FUN__text__00519d90(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 0x36) == '\x01') {
    *(undefined *)(param_1 + 0x69) = (&DAT_0075c700)[(uint)*(byte *)(param_1 + 0x51) * 6];
  }
  return;
}

