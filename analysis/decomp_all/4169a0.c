
void __thiscall
FUN__text__004169a0(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1 == 0) {
    local_10 = 0;
  }
  else {
    local_10 = param_1 + 0x844;
  }
  local_8 = param_1;
  local_c = FUN__text__0041ebf0(*(undefined4 *)(param_1 + 0xb210),local_10,param_3,param_4,1);
  local_8 = 0x416a0a;
  FUN__text__0056ce80();
  return;
}

