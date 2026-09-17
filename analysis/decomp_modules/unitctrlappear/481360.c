
void __thiscall FUN__text__00481360(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  char *local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (char *)(param_1 + 0x108f48);
  local_8 = param_1;
  FUN__text__004813f0(param_2,(int)*local_c,0);
  if ('\b' < *local_c) {
    FUN__text__004813f0(param_2,(int)*local_c,8);
  }
  if ('\x10' < *local_c) {
    FUN__text__004813f0(param_2,(int)*local_c,0x10);
  }
  local_8 = 0x4813ea;
  FUN__text__0056ce80();
  return;
}

