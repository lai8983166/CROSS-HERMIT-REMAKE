
undefined4 FUN__text__004593f0(undefined4 param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 < 0x1d) {
    if (param_2 == 0x1c) {
      return 1;
    }
    if ((param_2 == 2) || (param_2 == 0x10)) {
      return 1;
    }
  }
  else if (param_2 == 0x110) {
    return 1;
  }
  return 0;
}

