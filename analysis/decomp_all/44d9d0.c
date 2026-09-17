
int FUN__text__0044d9d0(short param_1,short param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [17];
  int local_24;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_24 = 0;
  while( true ) {
    if (local_24 == param_4) {
      return -1;
    }
    if (((((int)param_1 + (int)*(short *)(param_3 + local_24 * 8) < *(int *)(DAT_007a49fc + 0x196c))
         && (*(int *)(DAT_007a49fc + 0x196c) <
             (int)param_1 + (int)*(short *)(param_3 + local_24 * 8) +
             (int)*(short *)(param_3 + 4 + local_24 * 8))) &&
        ((int)param_2 + (int)*(short *)(param_3 + 2 + local_24 * 8) <
         *(int *)(DAT_007a49fc + 0x1970))) &&
       (*(int *)(DAT_007a49fc + 0x1970) <
        (int)param_2 + (int)*(short *)(param_3 + 2 + local_24 * 8) +
        (int)*(short *)(param_3 + 6 + local_24 * 8))) break;
    local_24 = local_24 + 1;
  }
  return local_24;
}

