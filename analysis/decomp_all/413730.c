
void __thiscall FUN__text__00413730(int param_1,undefined4 param_2,undefined4 param_3)

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
  *(undefined4 *)(param_1 + 0xb1f8) = 1;
  *(undefined4 *)(param_1 + 0xb1fc) = 0x40;
  local_8 = param_1;
  local_c = FUN__text__00413850(param_2,param_3);
  if (local_c == 0) {
    local_c = 0;
  }
  else {
    *(undefined4 *)(local_8 + 0xb1f8) = 1;
    *(undefined4 *)(local_8 + 0xb1fc) = 0x20;
    local_c = FUN__text__00413850(param_2,param_3);
    if (local_c == 0) {
      local_c = 0;
    }
    else {
      *(undefined4 *)(local_8 + 0xb1f8) = 2;
      *(undefined4 *)(local_8 + 0xb1fc) = 0x40;
      local_c = FUN__text__00413850(param_2,param_3);
      if (local_c == 0) {
        local_c = 0;
      }
      else {
        *(undefined4 *)(local_8 + 0xb1f8) = 2;
        *(undefined4 *)(local_8 + 0xb1fc) = 0x20;
        local_c = FUN__text__00413850(param_2,param_3);
      }
    }
  }
  local_8 = 0x41383e;
  FUN__text__0056ce80();
  return;
}

