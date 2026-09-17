
void __fastcall FUN__text__00481610(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  byte local_10;
  byte local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x2f156) == '\0') {
    local_10 = *(byte *)(param_1 + 0x2f15b);
    if ((local_10 != 0) && (local_10 < 3)) {
      FUN__text__004815c0();
    }
  }
  else {
    local_c = *(byte *)(param_1 + 0x2f15b);
    if (local_c < 2) {
      FUN__text__004816c0();
    }
    else if (local_c == 2) {
      FUN__text__00481810();
    }
  }
  local_8 = 0x4816b7;
  FUN__text__0056ce80();
  return;
}

