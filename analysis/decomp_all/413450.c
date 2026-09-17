
void __thiscall
FUN__text__00413450(int param_1,undefined4 param_2,undefined4 param_3,int param_4,undefined4 param_5
                   ,undefined4 param_6)

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
  *(undefined4 *)(param_1 + 0xb278) = param_5;
  *(undefined4 *)(param_1 + 0xb27c) = param_6;
  local_8 = param_1;
  local_c = FUN__text__004136d0();
  if (local_c == 0) {
    if (param_4 == 1) {
      local_c = FUN__text__00413730(param_2,param_3);
    }
    else {
      local_c = FUN__text__00413850(param_2,param_3);
    }
    if ((local_c == 0) && (local_c = FUN__text__00415f50(), local_c == 0)) {
      FUN__text__0040d970(local_8);
      local_c = FUN__text__0040dab0();
      if (local_c == 0) {
        FUN__text__00416c40(local_8 + 0xb408);
        FUN__text__00416cc0(local_8 + 0xb408);
      }
    }
  }
  local_8 = 0x413555;
  FUN__text__0056ce80();
  return;
}

