
undefined4 FUN__text__00429820(byte param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [16];
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1 < 0x7f) {
    uVar1 = 0;
  }
  else if ((param_1 < 0xa1) || (0xde < param_1)) {
    if ((param_1 < 0x81) || (0x9e < param_1)) {
      if ((param_1 < 0xe0) || (0xfb < param_1)) {
        uVar1 = 0;
      }
      else {
        uVar1 = 1;
      }
    }
    else {
      uVar1 = 1;
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

