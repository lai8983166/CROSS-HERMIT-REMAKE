
void FUN__text__004aa0e0(short param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [17];
  short local_c;
  
  sVar1 = DAT_007a5b62;
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  while ((local_c < DAT_007a5b62 && (*(short *)(&DAT_007a5662 + local_c * 0x10) != param_1))) {
    local_c = local_c + 1;
  }
  for (; (int)local_c < sVar1 + -1; local_c = local_c + 1) {
    *(undefined2 *)(&DAT_007a5662 + local_c * 0x10) =
         *(undefined2 *)(&DAT_007a5662 + (local_c + 1) * 0x10);
    (&DAT_007a5665)[local_c * 0x10] = (&DAT_007a5665)[(local_c + 1) * 0x10];
    (&DAT_007a5666)[local_c * 0x10] = (&DAT_007a5666)[(local_c + 1) * 0x10];
    (&DAT_007a5668)[local_c * 0x10] = (&DAT_007a5668)[(local_c + 1) * 0x10];
    (&DAT_007a5667)[local_c * 0x10] = (&DAT_007a5667)[(local_c + 1) * 0x10];
    *(undefined2 *)(&DAT_007a566a + local_c * 0x10) =
         *(undefined2 *)(&DAT_007a566a + (local_c + 1) * 0x10);
    *(undefined2 *)(&DAT_007a566c + local_c * 0x10) =
         *(undefined2 *)(&DAT_007a566c + (local_c + 1) * 0x10);
    *(undefined2 *)(&DAT_007a566e + local_c * 0x10) =
         *(undefined2 *)(&DAT_007a566e + (local_c + 1) * 0x10);
    *(undefined2 *)(&DAT_007a5670 + local_c * 0x10) =
         *(undefined2 *)(&DAT_007a5670 + (local_c + 1) * 0x10);
  }
  DAT_007a5b62 = DAT_007a5b62 + -1;
  return;
}

