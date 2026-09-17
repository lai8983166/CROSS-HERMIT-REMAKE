
void FUN__text__004cde10(undefined4 param_1,ushort param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0042ae20(param_1);
  if (*(char *)(local_8 + 0x92a0 + (uint)param_2) == '\x01') {
    FUN__text__0041f4e0(param_2);
  }
  FUN__text__00416790(local_c,param_2);
  *(undefined1 *)(local_8 + 0x92a0 + (uint)param_2) = 1;
  local_10 = local_c;
  FUN__text__00428ad0(local_c);
  local_8 = 0x4cdebd;
  FUN__text__0056ce80();
  return;
}

