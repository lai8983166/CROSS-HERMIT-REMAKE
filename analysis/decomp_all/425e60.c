
void FUN__text__00425e60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  iVar1 = FUN__text__00425c70();
  if (iVar1 == 0) {
    if (param_1 != 0) {
      local_c = FUN__text__00425cc0(1);
    }
  }
  else if (param_1 == 0) {
    local_c = FUN__text__00425cc0(0);
  }
  local_8 = 0x425ec8;
  FUN__text__0056ce80();
  return;
}

