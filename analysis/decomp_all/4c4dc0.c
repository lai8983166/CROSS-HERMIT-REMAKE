
void FUN__text__004c4dc0(int param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  short *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 4) >> 0x1c,
                              *(uint *)(param_2 + 4) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9250) = uVar1;
  iVar2 = *(int *)(local_8 + 0x9250) * 0x26;
  local_10 = (short *)(&DAT_00624520 + iVar2);
  *(char *)(local_8 + 0x1cc) = (char)*local_10;
  *(undefined2 *)(local_8 + 0x34 + param_1 * 0x1c8) = *(undefined2 *)(&DAT_00624532 + iVar2);
  *(undefined2 *)(local_8 + 0x36 + param_1 * 0x1c8) = *(undefined2 *)(&DAT_00624534 + iVar2);
  *(int *)(local_8 + 0x38 + param_1 * 0x1c8) = local_8 + 0x6f60 + *local_10 * 0xe0;
  local_8 = 0x4c4eaa;
  FUN__text__0056ce80();
  return;
}

