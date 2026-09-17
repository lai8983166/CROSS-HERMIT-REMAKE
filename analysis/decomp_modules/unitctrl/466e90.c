
void FUN__text__00466e90(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__00466da0(param_1,param_2);
  if (local_c == 0) {
    local_c = FUN__text__00466b40();
    FUN__text__00466c80(local_c,param_1,param_2);
  }
  local_8 = 0x466efa;
  FUN__text__0056ce80();
  return;
}

