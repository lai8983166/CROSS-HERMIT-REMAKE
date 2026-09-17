
void __thiscall FUN__text__004063d0(int param_1,int *param_2)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  short local_14;
  short local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(short *)(param_1 + 0x38) != 0) && (*(short *)(param_1 + 0x3a) != 0)) &&
     (*(int *)(param_1 + 0x34) != 0)) {
    local_8 = param_1;
    FUN__text__00403730();
    local_10 = FUN__text__00403b70(CONCAT22(extraout_var,*(undefined2 *)(local_8 + 0x38)));
    local_14 = FUN__text__00403b70(CONCAT22(extraout_var_00,*(undefined2 *)(local_8 + 0x3a)));
    (**(code **)(*param_2 + 100))
              (param_2,(int)local_10,(int)local_14,*(undefined4 *)(local_8 + 0x34),0,0,
               local_8 + 0x30);
    local_c = FUN__text__0056ce80();
  }
  local_8 = 0x406498;
  FUN__text__0056ce80();
  return;
}

