
void FUN__text__00410730(undefined4 param_1,undefined4 param_2,undefined2 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0040dcd0(9);
  *(undefined4 *)(local_c + 4) = 9;
  *(undefined4 *)(local_c + 8) = param_1;
  *(undefined4 *)(local_c + 0xc) = param_2;
  FUN__text__0040df20(local_c,param_3);
  local_8 = 0x4107a2;
  FUN__text__0056ce80();
  return;
}

