
void FUN__text__00440980(short param_1,short param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = (int)param_1;
  local_c = __ftol();
  local_18 = (int)param_2;
  local_10 = __ftol();
  local_c = local_c + -0x200;
  local_10 = local_10 + -0x11d;
  FUN__text__0043b460(local_c,local_10);
  local_8 = 0x440a08;
  FUN__text__0056ce80();
  return;
}

