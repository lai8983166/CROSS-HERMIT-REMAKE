
void __fastcall FUN__text__004567f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  void *local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (void *)(*(int *)(param_1 + 0x60) + 0x2450);
  local_8 = param_1;
  _memset(local_c,0,0x40);
  for (local_10 = 0; local_10 != 0x20; local_10 = local_10 + 1) {
    FUN__text__00456870((void *)((int)local_c + local_10 * 2));
  }
  local_8 = 0x456865;
  FUN__text__0056ce80();
  return;
}

