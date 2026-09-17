
void __fastcall FUN__text__0044ad50(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  short *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = (short *)(param_1 + 0x1a88);
  local_8 = param_1;
  local_c = FUN__text__0044c200((int)*local_10);
  local_14 = (int)*(char *)(local_c + 7);
  local_8 = 0x44ada4;
  FUN__text__0056ce80();
  return;
}

