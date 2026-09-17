
void FUN__text__004d12d0(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 4) >> 0x1c,
                              *(uint *)(param_2 + 4) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9250) = uVar1;
  FUN__text__004e3170(*(undefined2 *)(local_8 + 0x9250));
  local_8 = 0x4d134b;
  FUN__text__0056ce80();
  return;
}

