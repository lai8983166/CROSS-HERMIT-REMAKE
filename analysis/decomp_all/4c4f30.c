
void FUN__text__004c4f30(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = param_2;
  local_c = *(uint *)(param_2 + 4) >> 0x1c;
  local_10 = *(uint *)(param_2 + 4) & 0xfffffff;
  uVar1 = FUN__text__004c1eb0(param_1,local_c,local_10);
  *(undefined4 *)(local_8 + 0x9250) = uVar1;
  if (*(char *)(local_8 + 0x1cc) != -1) {
    FUN__text__004caf50(*(undefined2 *)(local_8 + 0x9250));
  }
  local_8 = 0x4c4fe7;
  FUN__text__0056ce80();
  return;
}

