
void __thiscall FUN__text__004c51a0(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_3;
  if (*(char *)(param_1 + 0x1cc) != -1) {
    local_8 = param_1;
    FUN__text__004cb120(0xffffffff,0xffffffff);
  }
  local_8 = 0x4c5211;
  FUN__text__0056ce80();
  return;
}

