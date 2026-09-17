
void FUN__text__00458800(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__004128f0(1,1);
  if (iVar1 == 0) {
    local_c = *(int *)(DAT_007a49fc + 0x196c);
    local_10 = *(int *)(DAT_007a49fc + 0x1970);
    local_28 = -1;
    for (local_24 = 0; local_24 != 2; local_24 = local_24 + 1) {
      local_14 = param_1 + *(short *)(&DAT_0060cb18 + local_24 * 8);
      local_18 = param_2 + *(short *)(&DAT_0060cb1a + local_24 * 8);
      local_1c = param_1 + *(short *)(&DAT_0060cb18 + local_24 * 8) +
                 (int)*(short *)(&DAT_0060cb1c + local_24 * 8);
      local_20 = param_2 + *(short *)(&DAT_0060cb1a + local_24 * 8) +
                 (int)*(short *)(&DAT_0060cb1e + local_24 * 8);
      if ((((local_14 < local_c) && (local_c < local_1c)) && (local_18 < local_10)) &&
         (local_10 < local_20)) {
        local_28 = local_24;
        break;
      }
    }
  }
  local_8 = 0x458923;
  FUN__text__0056ce80();
  return;
}

