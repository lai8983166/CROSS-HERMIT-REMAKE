
void FUN__text__004059e0(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  int local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined1 local_10 [8];
  undefined4 local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = *(undefined4 *)(param_1 + 0x12);
  local_18 = *(undefined4 *)(param_1 + 0x16);
  local_1c = param_1 + *(int *)(param_1 + 10);
  iVar1 = FUN__text__00403910(local_10);
  if (iVar1 == 0) {
    FUN__text__00405bc0(param_1,local_10,local_14,local_18,param_2,param_3);
    FUN__text__00403990();
  }
  local_8 = 0x405a74;
  FUN__text__0056ce80();
  return;
}

