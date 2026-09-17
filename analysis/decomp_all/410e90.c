
void __thiscall FUN__text__00410e90(int param_1,undefined4 param_2,undefined4 param_3)

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
  *(undefined4 *)(param_1 + 0x378) = param_2;
  *(undefined4 *)(param_1 + 0x37c) = param_3;
  local_8 = param_1;
  FUN__text__00410db0();
  local_c = FUN__text__00410f30();
  if ((local_c == 0) && (local_c = FUN__text__00410f90(), local_c == 0)) {
    local_c = FUN__text__00411090();
  }
  local_8 = 0x410f24;
  FUN__text__0056ce80();
  return;
}

