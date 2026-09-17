
void FUN__text__0049ad90(int param_1,int param_2)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  uint local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__0046a4c0(param_1);
  if (((iVar2 == 0) || (local_14 = (uint)*(ushort *)(*(int *)(param_1 + 600) + 2), local_14 == 0))
     || (0xc < local_14)) goto LAB__text__0049b00c;
  local_c = local_14 + 6;
  if (param_2 < 100) {
    cVar1 = (&DAT_0061a394)[param_2];
  }
  else {
    cVar1 = *(char *)((int)&PTR_PTR_0061a358 + param_2);
  }
  local_10 = (int)cVar1;
  if (local_10 == -1) goto LAB__text__0049b00c;
  local_18 = FUN__text__00467e70();
  local_18 = local_18 % 100;
  local_1c = param_2 + -3;
  switch(param_2) {
  case 3:
  case 0x70:
  case 0x71:
  case 0x96:
    break;
  case 4:
  case 0x68:
    goto joined_r0x0049ae77;
  default:
    goto joined_r0x0049ae77;
  case 0x19:
  case 0x65:
    goto joined_r0x0049ae77;
  case 0x6a:
    if (local_18 < 0x50) goto LAB__text__0049b00c;
    break;
  case 0x6c:
  case 0x6d:
  case 0x6e:
    if (local_18 < 0x28) goto LAB__text__0049b00c;
    break;
  case 0x72:
joined_r0x0049ae77:
    if (local_18 < 0x32) goto LAB__text__0049b00c;
    break;
  case 0x7d:
    if (local_18 < 0x3c) goto LAB__text__0049b00c;
    break;
  case 0x94:
  case 0x95:
    if (local_18 < 0x46) goto LAB__text__0049b00c;
    break;
  case 0x97:
    if (local_18 < 0x37) goto LAB__text__0049b00c;
  }
  local_18 = FUN__text__00467e70();
  local_18 = local_18 % 100;
  local_20 = local_10 + -6;
  switch(local_10) {
  case 6:
    if (local_18 < 0x28) {
      local_10 = 0x2f;
    }
    break;
  case 9:
    if (local_18 < 0x32) {
      local_10 = 8;
    }
    break;
  case 0x26:
    if (local_18 < 0x32) {
      local_10 = 0x27;
    }
    break;
  case 0x27:
    if (local_18 < 0x32) {
      local_10 = 0x26;
    }
    break;
  case 0x2f:
    if (local_18 < 0x3c) {
      local_10 = 6;
    }
  }
  local_24 = local_10 + -2;
  switch(local_10) {
  case 2:
    local_10 = 4;
    break;
  default:
    goto LAB__text__0049b00c;
  case 4:
    local_10 = 5;
    break;
  case 6:
    local_10 = 0;
    break;
  case 7:
    local_10 = 1;
    break;
  case 8:
    local_10 = 2;
    break;
  case 0x1f:
  case 0x20:
    local_10 = 6;
    break;
  case 0x22:
    local_10 = 8;
    break;
  case 0x24:
    local_10 = 7;
    break;
  case 0x2f:
    local_10 = 3;
  }
  FUN__text__0040d390(local_c,local_10,local_14 + 9,0);
LAB__text__0049b00c:
  local_8 = 0x49b019;
  FUN__text__0056ce80();
  return;
}

