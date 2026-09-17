
void FUN__text__00472860(short param_1,short param_2,undefined2 param_3)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0046b130(param_1,CONCAT22(0xcccc,param_2));
  if (iVar1 != 0) {
    FUN__text__0040a330(local_8 + 0x109388,local_8 + 0xde4b0,(int)param_1,(int)param_2,
                        CONCAT22(extraout_var,param_3));
  }
  local_8 = 0x4728d0;
  FUN__text__0056ce80();
  return;
}

