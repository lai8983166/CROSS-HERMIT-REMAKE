
void __thiscall FUN__text__00403d50(int param_1,int *param_2)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
  undefined4 *puVar2;
  undefined4 local_74 [16];
  undefined1 local_34 [24];
  undefined2 local_1c;
  undefined2 local_18;
  short local_14;
  short local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_74;
  for (iVar1 = 0x1c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(short *)(param_1 + 0x38) != 0) && (*(short *)(param_1 + 0x3a) != 0)) &&
     (*(int *)(param_1 + 0x34) != 0)) {
    local_8 = param_1;
    FUN__text__00403730();
    local_10 = FUN__text__00403b70(CONCAT22(extraout_var,*(undefined2 *)(local_8 + 0x38)));
    local_14 = FUN__text__00403b70(CONCAT22(extraout_var_00,*(undefined2 *)(local_8 + 0x3a)));
    (**(code **)(*param_2 + 0x50))
              (param_2,(int)local_10,(int)local_14,1,1,*(undefined4 *)(local_8 + 0x34),0,
               local_8 + 0x2c);
    local_c = FUN__text__0056ce80();
    if (-1 < local_c) {
      (**(code **)(**(int **)(local_8 + 0x2c) + 0x38))(*(undefined4 *)(local_8 + 0x2c),0,local_34);
      local_c = FUN__text__0056ce80();
      if (-1 < local_c) {
        *(undefined2 *)(local_8 + 0x3c) = local_1c;
        *(undefined2 *)(local_8 + 0x3e) = local_18;
      }
      *(int **)(local_8 + 0x28) = param_2;
    }
  }
  local_8 = 0x403e61;
  FUN__text__0056ce80();
  return;
}

