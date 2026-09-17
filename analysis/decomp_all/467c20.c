
void __thiscall FUN__text__00467c20(int param_1,undefined2 param_2)

{
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  int iVar1;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN__text__00472f40(0x230,6,CONCAT22((short)((uint)(*(int *)(param_1 + 0x2e6f8) % 0x3c) >> 0x10),
                                       param_2),*(int *)(param_1 + 0x2e6f8) / 0x3c,0,1,0xffffffff,0)
  ;
  if (*(int *)(local_8 + 0x2e6fc) == 0x7fffffff) {
    FUN__text__00473570(0x148,6,CONCAT22(extraout_var_01,param_2),0,1,0xffffffff);
    FUN__text__00473570(0x18e,6,CONCAT22(extraout_var_02,param_2),0,1,0xffffffff);
    FUN__text__00473390(0x184,6,CONCAT22(extraout_var,param_2),1,0xffffffff);
  }
  else {
    FUN__text__00472f40(0x148,6,CONCAT22((short)((uint)(*(int *)(local_8 + 0x2e6f4) % 0x3c) >> 0x10)
                                         ,param_2),*(int *)(local_8 + 0x2e6f4) / 0x3c,0,1,0xffffffff
                        ,0);
    FUN__text__00472f40(0x18e,6,CONCAT22((short)((uint)(*(int *)(local_8 + 0x2e6fc) % 0x3c) >> 0x10)
                                         ,param_2),*(int *)(local_8 + 0x2e6fc) / 0x3c,0,1,0xffffffff
                        ,0);
    FUN__text__00473390(0x184,6,CONCAT22(extraout_var_00,param_2),1,0xffffffff);
  }
  local_8 = 0x467d49;
  FUN__text__0056ce80();
  return;
}

