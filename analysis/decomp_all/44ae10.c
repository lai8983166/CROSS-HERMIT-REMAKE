
void __fastcall FUN__text__0044ae10(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_10 = 0; local_10 != 0x1e; local_10 = local_10 + 1) {
    *(undefined1 *)(param_1 + local_10 * 8 + 0x1ab1) = 0;
  }
  return;
}

