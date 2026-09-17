
void FUN__text__0042af00(undefined4 param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 1;
  local_8 = FUN__text__0056e7c0(param_1,&DAT_00595078);
  if (local_8 != 0) {
    local_c = FUN__text__00570d70(param_2,1,param_3,local_8);
    if (local_c == param_3) {
      local_10 = 0;
    }
  }
  FUN__text__00586030();
  local_8 = 0x42af76;
  FUN__text__0056ce80();
  return;
}

