
void FUN__text__004d6710(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c < 100; local_c = local_c + 1) {
    FUN__text__004d6770(local_c);
  }
  local_8 = 0x4d6766;
  FUN__text__0056ce80();
  return;
}

