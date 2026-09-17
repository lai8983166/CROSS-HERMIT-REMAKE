
int FUN__text__004d5850(int param_1)

{
  byte bVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [17];
  short local_10;
  int local_c;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  for (local_10 = 0; local_10 < 0x54; local_10 = local_10 + 1) {
    bVar1 = *(byte *)(param_1 + 8 + local_10 * 0xc);
    if ((bVar1 == 3) || ((4 < bVar1 && (bVar1 < 7)))) {
      local_c = local_c + *(int *)(&DAT_006c2e08 + (local_10 + 1) * 0x48);
    }
  }
  return local_c;
}

