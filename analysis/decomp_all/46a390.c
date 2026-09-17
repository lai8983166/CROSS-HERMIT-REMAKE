
void FUN__text__0046a390(int param_1)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00468d10(param_1);
  if (iVar2 != 0) {
    uVar1 = *(ushort *)(*(int *)(param_1 + 600) + 2);
    local_c = uVar1 - 0x1b9;
    switch(uVar1) {
    case 0x1b9:
    case 0x1ba:
    case 0x1bb:
    case 0x1bc:
    case 0x1bd:
    case 0x1be:
    case 0x1bf:
    case 0x1c1:
    case 0x1c2:
      break;
    default:
    }
  }
  local_8 = 0x46a40d;
  FUN__text__0056ce80();
  return;
}

