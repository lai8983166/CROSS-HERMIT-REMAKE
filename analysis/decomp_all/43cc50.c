
void __fastcall FUN__text__0043cc50(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(undefined4 *)(DAT_007a49fc + 0x19bc);
  local_10 = *(int *)(DAT_007a49fc + 0x19c0);
  if (local_10 < 0x1e) {
    local_10 = 0x1e;
  }
  if (599 < local_10) {
    local_10 = 599;
  }
  *(undefined4 *)(param_1 + 0x265b8) = local_c;
  *(undefined4 *)(param_1 + 0x265c0) = local_c;
  *(int *)(param_1 + 0x265bc) = local_10;
  *(int *)(param_1 + 0x265c4) = local_10;
  local_8 = param_1;
  iVar1 = FUN__text__0056db00(*(int *)(param_1 + 0x265b8) - *(int *)(param_1 + 0x265c0));
  *(int *)(local_8 + 0x265d0) = iVar1 / 2;
  iVar1 = FUN__text__0056db00(*(int *)(local_8 + 0x265bc) - *(int *)(local_8 + 0x265c4));
  *(int *)(local_8 + 0x265d4) = iVar1 / 2;
  *(int *)(local_8 + 0x265c8) = *(int *)(local_8 + 0x265b8) + *(int *)(local_8 + 0x265d0);
  *(int *)(local_8 + 0x265cc) = *(int *)(local_8 + 0x265bc) + *(int *)(local_8 + 0x265d4);
  local_8 = 0x43cd6c;
  FUN__text__0056ce80();
  return;
}

