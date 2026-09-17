
void FUN__text__004168e0(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__0042ae20(param_2);
  if (local_10 != 0) {
    local_c = local_10;
    local_14 = FUN__text__004214f0(local_10,0);
    local_18 = FUN__text__004214f0(local_c,1);
    if (local_8 == 0) {
      local_20 = 0;
    }
    else {
      local_20 = local_8 + 0x844;
    }
    local_1c = FUN__text__0041ebf0(*(undefined4 *)(local_8 + 0xb210),local_20,local_14,local_18,1);
  }
  local_8 = 0x41698f;
  FUN__text__0056ce80();
  return;
}

