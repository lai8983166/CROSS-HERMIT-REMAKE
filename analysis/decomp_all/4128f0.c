
undefined4 __thiscall FUN__text__004128f0(int param_1,uint param_2,undefined4 param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [18];
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  switch(param_3) {
  case 0:
    if ((*(byte *)(param_1 + 0x480 + (param_2 & 0xff)) & 0x80) == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
    break;
  case 1:
    if ((*(byte *)(param_1 + 0x580 + (param_2 & 0xff)) & 0x80) == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
    break;
  case 2:
    if ((*(byte *)(param_1 + 0x680 + (param_2 & 0xff)) & 0x80) == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
    break;
  case 3:
    if ((*(byte *)(param_1 + 0x380 + (param_2 & 0xff)) & 0x80) == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
    break;
  case 4:
    if ((*(byte *)(param_1 + 0x780 + (param_2 & 0xff)) & 0x80) == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
    break;
  default:
    uVar1 = 0;
  }
  return uVar1;
}

