
void FUN__text__00437d90(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x2f4;
  local_10 = param_1 + 0x3e0;
  iVar1 = FUN__text__00437d10(param_1);
  if (((iVar1 == 0) && (*(int *)(local_8 + 0x60) != 0)) &&
     ((*(int *)(local_c + 4) == *(int *)(local_8 + 0x60) ||
      (*(int *)(local_10 + 4) == *(int *)(local_8 + 0x60))))) {
    FUN__text__00439c60();
    if (param_2 == 0) {
      FUN__text__00437c90(local_c);
    }
    FUN__text__00437c90(local_10);
  }
  local_8 = 0x437e38;
  FUN__text__0056ce80();
  return;
}

