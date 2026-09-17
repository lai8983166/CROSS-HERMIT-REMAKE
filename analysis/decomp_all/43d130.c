
void __fastcall FUN__text__0043d130(int param_1)

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
  local_c = *(undefined4 *)(param_1 + 0xa4);
  *(undefined4 *)(param_1 + 0xa4) = *(undefined4 *)(param_1 + 0xa8);
  *(undefined4 *)(param_1 + 0xa8) = local_c;
  local_8 = param_1;
  FUN__text__0043d0c0(*(undefined4 *)(param_1 + 0xa4));
  local_8 = 0x43d196;
  FUN__text__0056ce80();
  return;
}

