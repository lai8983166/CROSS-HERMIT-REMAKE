
void __fastcall FUN__text__00410f90(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    (**(code **)(*(int *)*param_1 + 0xc))(*param_1,&DAT_005cc04c,param_1 + 1,0);
    local_c = FUN__text__0056ce80();
    if (local_c == 0) {
      (**(code **)(*(int *)local_8[1] + 0x2c))(local_8[1],&DAT_005cac3c);
      local_c = FUN__text__0056ce80();
      if (local_c == 0) {
        (**(code **)(*(int *)local_8[1] + 0x34))(local_8[1],PTR_DAT_007a0bb4,6);
        local_c = FUN__text__0056ce80();
        if (local_c == 0) {
          (**(code **)(*(int *)local_8[1] + 0x1c))(local_8[1]);
          local_c = FUN__text__0056ce80();
        }
      }
    }
  }
  local_8 = (int *)0x41108a;
  FUN__text__0056ce80();
  return;
}

