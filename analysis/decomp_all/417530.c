
void FUN__text__00417530(void)

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
  FUN__text__00420990();
  for (local_c = 0; local_c != 100; local_c = local_c + 1) {
    *(undefined4 *)(local_8 + local_c * 8) = 0;
    *(undefined4 *)(local_8 + 4 + local_c * 8) = 0;
  }
  local_8 = 0x41759a;
  FUN__text__0056ce80();
  return;
}

