
void FUN__text__004b7e20(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined4 param_4
                        ,undefined2 param_5,undefined2 param_6,undefined2 param_7,undefined2 param_8
                        ,undefined2 param_9)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004b7e90(param_1,param_2,CONCAT22(0xcccc,param_3),param_4,param_5,
                      CONCAT22(0xcccc,param_6),param_7,param_8,CONCAT22(0xcccc,param_9),1);
  local_8 = 0x4b7e80;
  FUN__text__0056ce80();
  return;
}

