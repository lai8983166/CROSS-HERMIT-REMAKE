
void __fastcall FUN__text__0041e3d0(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((((*param_1 != 0) && (param_1[1] != 0)) && (param_1[2] != 0)) &&
      ((param_1[3] != 0 && (param_1[4] != 0)))) &&
     ((param_1[5] != 0 && (local_8 = param_1, iVar1 = FUN__text__0041d790(), iVar1 != 0)))) {
    (**(code **)(*(int *)local_8[1] + 0x28))(local_8[1],4,&local_10);
    local_14 = FUN__text__0056ce80();
    local_c = local_14;
    if ((local_14 != -0x7fffbffb) && (local_14 == 0)) {
      local_18 = local_10;
    }
  }
  local_8 = (int *)0x41e4f1;
  FUN__text__0056ce80();
  return;
}

