
void FUN__text__0040a390(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        ,undefined2 param_5,undefined2 param_6,undefined2 param_7)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0040a1e0();
  FUN__text__0040a220(param_1);
  FUN__text__0040a290(param_2,param_3,param_4,CONCAT22(extraout_var,param_5),
                      CONCAT22(extraout_var_01,param_6),CONCAT22(extraout_var_00,param_7));
  local_8 = 0x40a3f1;
  FUN__text__0056ce80();
  return;
}

