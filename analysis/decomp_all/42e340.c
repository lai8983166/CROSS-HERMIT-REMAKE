
void FUN__text__0042e340(undefined4 param_1,int param_2)

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
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 8) >> 0x1c,
                              *(uint *)(local_c + 8) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9254) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0xc) >> 0x1c,
                              *(uint *)(local_c + 0xc) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9258) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x10) >> 0x1c,
                              *(uint *)(local_c + 0x10) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x925c) = uVar1;
  FUN__text__004988d0(*(undefined4 *)(local_8 + 0x9250),*(undefined4 *)(local_8 + 0x9254),
                      *(undefined4 *)(local_8 + 0x9258),*(undefined4 *)(local_8 + 0x925c));
  local_8 = 0x42e45c;
  FUN__text__0056ce80();
  return;
}

