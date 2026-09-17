
void __fastcall FUN__text__00416c40(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != 0x100; local_c = local_c + 1) {
    *(short *)(param_1 + 0xb408 + local_c * 2) = (short)(local_c << 8);
    *(short *)(param_1 + 0xb608 + local_c * 2) = (short)(local_c << 8);
    *(short *)(param_1 + 0xb808 + local_c * 2) = (short)(local_c << 8);
  }
  return;
}

