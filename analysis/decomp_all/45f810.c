
int FUN__text__0045f810(void)

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
    if (local_24 == 6) {
      return -1;
    }
    if (((((int)*(short *)(&DAT_0060ceb0 + local_24 * 8) < *(int *)(DAT_007a49fc + 0x196c)) &&
         (*(int *)(DAT_007a49fc + 0x196c) <
          (int)*(short *)(&DAT_0060ceb0 + local_24 * 8) +
          (int)*(short *)(&DAT_0060ceb4 + local_24 * 8))) &&
        ((int)*(short *)(&DAT_0060ceb2 + local_24 * 8) < *(int *)(DAT_007a49fc + 0x1970))) &&
       (*(int *)(DAT_007a49fc + 0x1970) <
        (int)*(short *)(&DAT_0060ceb2 + local_24 * 8) +
        (int)*(short *)(&DAT_0060ceb6 + local_24 * 8))) break;
    local_24 = local_24 + 1;
  }
  return local_24;
}

