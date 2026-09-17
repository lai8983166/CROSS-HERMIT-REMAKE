
void FUN__text__00428ff0(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 1;
  local_14 = param_3;
  local_c = FUN__text__00428e80(param_1,&local_10,param_2,&local_14);
  local_8 = 0x429051;
  FUN__text__0056ce80();
  return;
}

