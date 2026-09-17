
void FUN__text__0048dcd0(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(undefined4 *)(param_2 + 8);
  iVar1 = FUN__text__0048e1b0(local_c);
  if ((iVar1 == 0) && (iVar1 = FUN__text__0048e140(local_c), iVar1 == 0)) {
    FUN__text__0048df50(param_1);
  }
  FUN__text__0048dd60(param_1,param_2);
  FUN__text__00427cd0(param_2);
  local_8 = 0x48dd57;
  FUN__text__0056ce80();
  return;
}

