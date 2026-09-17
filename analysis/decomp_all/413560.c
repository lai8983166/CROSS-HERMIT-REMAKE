
void __fastcall FUN__text__00413560(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_c = FUN__text__00410e90(*(undefined4 *)(param_1 + 0xb278),*(undefined4 *)(param_1 + 0xb27c))
  ;
  local_8 = 0x4135be;
  FUN__text__0056ce80();
  return;
}

