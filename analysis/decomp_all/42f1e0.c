
void FUN__text__0042f1e0(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  local_10 = 0;
  local_14 = param_2;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 4) >> 0x1c,
                              *(uint *)(param_2 + 4) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9250) = uVar1;
  FUN__text__00499110(*(undefined4 *)(local_8 + 0x9250),&local_c,&local_10);
  FUN__text__004c1f40(param_1,*(uint *)(local_14 + 4) >> 0x1c,*(uint *)(local_14 + 4) & 0xfffffff,
                      local_c);
  FUN__text__004c1f40(param_1,*(uint *)(local_14 + 8) >> 0x1c,*(uint *)(local_14 + 8) & 0xfffffff,
                      local_10);
  local_8 = 0x42f2be;
  FUN__text__0056ce80();
  return;
}

