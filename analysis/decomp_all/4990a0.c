
void FUN__text__004990a0(undefined4 param_1,undefined4 param_2,short param_3,undefined4 param_4,
                        undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  uint local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_3 == 0) {
    local_8 = CONCAT22(local_8._2_2_,100);
  }
  else {
    local_8 = CONCAT22(local_8._2_2_,param_3);
  }
  FUN__text__00456340(param_1,param_2,local_8 & 0xffff,param_4,param_5);
  local_8 = 0x499101;
  FUN__text__0056ce80();
  return;
}

