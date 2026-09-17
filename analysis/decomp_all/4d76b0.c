
int FUN__text__004d76b0(char *param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  uint local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  for (local_c = 0; local_c < param_2; local_c = local_c + 1) {
    local_10 = local_10 + *param_1;
    param_1 = param_1 + 1;
  }
  return local_10;
}

