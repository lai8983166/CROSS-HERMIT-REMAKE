
void __thiscall FUN__text__004162c0(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined1 local_c [4];
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_10 = FUN__text__0052afe6(*(undefined4 *)(param_1 + 0xb210),param_2,local_c);
  local_8 = 0x416311;
  FUN__text__0056ce80();
  return;
}

