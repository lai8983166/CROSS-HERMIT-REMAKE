
void FUN__text__0044b550(undefined2 param_1,undefined2 param_2)

{
  int iVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0044ac50();
  FUN__text__0044cc80(CONCAT22(extraout_var_00,param_1),CONCAT22(extraout_var,param_2),0x55,local_c,
                      2);
  local_8 = 0x44b59f;
  FUN__text__0056ce80();
  return;
}

