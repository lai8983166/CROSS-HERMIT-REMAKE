
void FUN__text__00460d50(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  while ((*(uint *)(DAT_007a49fc + 0x1990) & 1) == 0) {
    FUN__text__004610f0(param_1);
    FUN__text__004615a0();
    FUN__text__00422360(0);
  }
  FUN__text__004db2b0(0);
  local_8 = 0x460dc4;
  FUN__text__0056ce80();
  return;
}

