
undefined4 __fastcall FUN__text__00421660(int param_1)

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
  for (local_c = 0; local_c != 0x20; local_c = local_c + 1) {
    *(undefined4 *)(param_1 + 4 + local_c * 8) = 0;
    *(undefined4 *)(param_1 + local_c * 8) = 0;
  }
  return 0;
}

