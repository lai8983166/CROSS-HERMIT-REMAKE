
void FUN__text__0041fd10(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0041fa50();
  local_c = FUN__text__0042ae20(param_1);
  if (local_c != 0) {
    local_10 = FUN__text__0041fe00(local_c,param_2);
    if ((local_10 == 0) && (param_2 != 0)) {
      local_10 = FUN__text__00420210(local_c);
    }
    local_14 = local_c;
    FUN__text__00428ad0(local_c);
  }
  local_8 = 0x41fdb1;
  FUN__text__0056ce80();
  return;
}

