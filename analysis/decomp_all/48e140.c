
undefined4 FUN__text__0048e140(undefined1 *param_1)

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
  switch(*param_1) {
  case 9:
  case 10:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0x11:
    uVar1 = 1;
    break;
  default:
    uVar1 = 0;
  }
  return uVar1;
}

