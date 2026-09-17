
void FUN__text__004586d0(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__00458800(param_1,param_2);
  if (local_c == 2) {
    local_c = 0;
LAB__text__0045872b:
    FUN__text__004db2b0(5);
    local_10 = local_c;
    if (((local_c == 0) || (local_c == 1)) || (local_c == 2)) goto LAB__text__004587b1;
  }
  else if ((local_c != -1) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0))
  goto LAB__text__0045872b;
  FUN__text__00458930(param_1,param_2);
  if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) != 0) {
    FUN__text__00458a50(param_1,param_2,local_c);
  }
  iVar1 = FUN__text__00454c40();
  if (iVar1 != 0) {
    FUN__text__00458f10();
  }
LAB__text__004587b1:
  local_8 = 0x4587be;
  FUN__text__0056ce80();
  return;
}

