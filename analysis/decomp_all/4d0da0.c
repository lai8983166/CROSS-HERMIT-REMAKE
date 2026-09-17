
void FUN__text__004d0da0(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined2 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 4) >> 0x1c,
                              *(uint *)(param_2 + 4) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9250) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 8) >> 0x1c,
                              *(uint *)(local_c + 8) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9254) = uVar1;
  local_10 = *(undefined2 *)(local_8 + 0x9250);
  local_14 = *(undefined4 *)(local_8 + 0x9254);
  switch(local_14) {
  case 0:
    DAT_007a528e = local_10;
    break;
  case 1:
    DAT_007a5290 = local_10;
    break;
  case 2:
    DAT_007a5292 = local_10;
    break;
  case 3:
    DAT_007e1180 = local_10;
    break;
  case 4:
    DAT_007e1182 = local_10;
  }
  local_8 = 0x4d0ea8;
  FUN__text__0056ce80();
  return;
}

