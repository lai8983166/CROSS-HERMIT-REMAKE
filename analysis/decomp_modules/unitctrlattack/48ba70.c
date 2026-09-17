
void FUN__text__0048ba70(undefined4 param_1,undefined4 param_2,int param_3,undefined4 param_4,
                        undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(byte *)(*(int *)(param_3 + 600) + 7) < 0x4b) {
    FUN__text__0048baf0(param_1,param_2,param_3,param_4,param_5);
  }
  else {
    FUN__text__0048be10(param_1,param_2,param_3,param_4,param_5);
  }
  local_8 = 0x48bae7;
  FUN__text__0056ce80();
  return;
}

