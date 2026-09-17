
void __fastcall FUN__text__00492e90(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 0x200; local_c = local_c + 1) {
    FUN__text__00492f00(local_8 + 0x2b6f0 + local_c * 8);
  }
  local_8 = 0x492eed;
  FUN__text__0056ce80();
  return;
}

