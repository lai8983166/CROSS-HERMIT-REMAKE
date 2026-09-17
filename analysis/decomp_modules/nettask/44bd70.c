
void FUN__text__0044bd70(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(&DAT_007a2988,0,0x100);
  for (local_c = 0; local_c != 2; local_c = local_c + 1) {
    for (local_10 = 0; local_10 != 0x40; local_10 = local_10 + 1) {
      *(undefined2 *)(&DAT_007a2988 + local_10 * 2 + local_c * 0x80) =
           *(undefined2 *)(&DAT_006000b0 + local_10 * 2 + local_c * 0x80);
    }
  }
  local_8 = 0x44be04;
  FUN__text__0056ce80();
  return;
}

