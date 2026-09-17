
undefined4 FUN__text__0046b1a0(short param_1,short param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [17];
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_2 < 0xe) {
    uVar1 = 0;
  }
  else if (param_2 < 0x289) {
    if (param_1 < -0x20) {
      uVar1 = 0;
    }
    else if (param_1 < 0x421) {
      uVar1 = 1;
    }
    else {
      uVar1 = 0;
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

