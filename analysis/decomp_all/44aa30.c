
void __thiscall FUN__text__0044aa30(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  undefined1 *local_10;
  undefined *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  _memset((void *)(param_1 + 0x1ab0),0,0xf0);
  if (0x1d < param_2) {
    param_2 = 0x1e;
  }
  for (local_14 = 0; local_14 != param_2; local_14 = local_14 + 1) {
    local_c = &DAT_007f4518 + local_14 * 0xb0;
    local_10 = (undefined1 *)(local_8 + 0x1ab0 + local_14 * 8);
    *local_10 = 1;
    local_10[1] = 0;
    *(undefined **)(local_10 + 4) = &DAT_007f4518 + local_14 * 0xb0;
  }
  local_8 = 0x44aadd;
  FUN__text__0056ce80();
  return;
}

