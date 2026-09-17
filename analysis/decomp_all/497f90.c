
void FUN__text__00497f90(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = (int)((int)*(short *)(DAT_007a49f8 + 0x24c0) +
                 ((int)*(short *)(DAT_007a49f8 + 0x24c0) >> 0x1f & 0x1fU)) >> 5;
  local_c = (int)((int)*(short *)(DAT_007a49f8 + 0x24c2) +
                 ((int)*(short *)(DAT_007a49f8 + 0x24c2) >> 0x1f & 0xfU)) >> 4;
  FUN__text__00498010(local_8,local_c,param_1);
  local_8 = 0x498006;
  FUN__text__0056ce80();
  return;
}

