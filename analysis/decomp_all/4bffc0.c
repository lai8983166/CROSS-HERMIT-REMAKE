
void __fastcall FUN__text__004bffc0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [19];
  short local_c;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 1; local_c < 0x55; local_c = local_c + 1) {
    if ((byte)(&DAT_006c2dcc)[local_c * 0x48] != 0) {
      *(short *)(param_1 + 0x136e +
                (short)(((byte)(&DAT_006c2dcc)[local_c * 0x48] - 1) +
                       ((byte)(&DAT_006c2dcf)[local_c * 0x48] - 1) * 0xc) * 2) = local_c;
    }
  }
  return;
}

