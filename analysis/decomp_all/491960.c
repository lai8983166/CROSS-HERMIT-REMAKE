
void __thiscall
FUN__text__00491960(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_4 + 0x40) != 0) {
    local_c = *(int *)(param_4 + 0x40);
    local_8 = param_1;
    do {
      local_10 = *(int *)(local_c + 4);
      local_14 = *(undefined4 *)(local_c + 8);
      local_18 = FUN__text__004919f0(param_2,param_3,local_14);
      if (local_18 != 0) {
        FUN__text__0040be20(local_c);
      }
      local_c = local_10;
    } while (local_10 != 0);
  }
  local_8 = 0x4919e9;
  FUN__text__0056ce80();
  return;
}

