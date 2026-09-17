
void FUN__text__00441ea0(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00419450();
  if (iVar1 != 0) {
    local_c = FUN__text__0041ae70();
    local_c = FUN__text__0041abf0(*param_1);
    if (local_c != 0) {
      *(undefined1 *)(local_c + 1) = 1;
    }
    local_10 = FUN__text__00442b30();
  }
  local_8 = 0x441f2c;
  FUN__text__0056ce80();
  return;
}

