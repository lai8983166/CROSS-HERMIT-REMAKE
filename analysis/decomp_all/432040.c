
void __thiscall FUN__text__00432040(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  local_8 = param_1;
  for (local_c = 0; *(short *)(param_2 + local_c * 2) != -1; local_c = local_c + 1) {
    local_14 = FUN__text__00431cc0((int)*(short *)(param_2 + local_c * 2));
    local_18 = local_8 + 0x80aec + local_14 * 0x520;
    iVar1 = FUN__text__00468d10(local_18);
    if (iVar1 != 0) {
      iVar1 = FUN__text__00469220(local_18);
      if (iVar1 != 0) {
        local_10 = local_10 + 1;
      }
    }
  }
  local_8 = 0x4320ec;
  FUN__text__0056ce80();
  return;
}

