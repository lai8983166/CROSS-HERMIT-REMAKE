
void __fastcall FUN__text__00468c00(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  puVar2 = &DAT_00618668;
  puVar3 = (undefined4 *)(param_1 + 0x115bac);
  for (iVar1 = 0x40; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = *puVar2;
    puVar2 = puVar2 + 1;
    puVar3 = puVar3 + 1;
  }
  for (local_c = 0; local_c != 4; local_c = local_c + 1) {
    for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
      if ((local_c != local_10) && ((&DAT_007f44e4)[local_c] == (&DAT_007f44e4)[local_10])) {
        *(undefined1 *)(param_1 + 0x115bac + local_10 + local_c * 0x10) = 0;
      }
    }
  }
  local_8 = param_1;
  FUN__text__00468cd0(param_1 + 0x115bac);
  local_8 = 0x468cbd;
  FUN__text__0056ce80();
  return;
}

