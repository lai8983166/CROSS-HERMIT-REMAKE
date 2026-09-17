
void FUN__text__00488af0(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004deaa0(param_2,param_3);
  FUN__text__0046b3e0(param_2,param_3);
  iVar1 = FUN__text__0046c9f0(param_1);
  if (iVar1 == 0) {
    local_c = &DAT_006c2dc8 + param_1 * 0x48;
    local_10 = FUN__text__004de8f0(param_1);
    FUN__text__0048a260(local_10,local_c,param_2,param_3);
    FUN__text__0048a380(local_10,local_c,param_2,param_3);
    FUN__text__0048a730(local_10,local_c,param_2,param_3);
  }
  local_8 = 0x488bb0;
  FUN__text__0056ce80();
  return;
}

