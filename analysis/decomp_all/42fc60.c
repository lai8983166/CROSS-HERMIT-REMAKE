
void FUN__text__0042fc60(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_2;
  local_10 = FUN__text__00496dc0();
  FUN__text__004c1f40(param_1,*(uint *)(local_c + 4) >> 0x1c,*(uint *)(local_c + 4) & 0xfffffff,
                      local_10);
  local_8 = 0x42fcc4;
  FUN__text__0056ce80();
  return;
}

