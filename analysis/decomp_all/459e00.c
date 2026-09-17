
void __fastcall FUN__text__00459e00(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [18];
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x30) = 2;
  local_8 = 0x459fa7;
  FUN__text__0056ce80();
  return;
}

