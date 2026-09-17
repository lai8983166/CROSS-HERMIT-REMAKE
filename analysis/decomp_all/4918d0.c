
void FUN__text__004918d0(int param_1,undefined4 param_2)

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
  FUN__text__00491960(param_1,param_2,param_1 + 0x48);
  for (local_c = 0; local_c != 5; local_c = local_c + 1) {
    FUN__text__00491960(param_1,param_2,param_1 + 0xa0 + local_c * 0x58);
  }
  local_8 = 0x49194c;
  FUN__text__0056ce80();
  return;
}

