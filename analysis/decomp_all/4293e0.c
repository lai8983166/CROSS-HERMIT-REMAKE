
void FUN__text__004293e0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [15];
  undefined4 uStack_10;
  undefined4 local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_FindWindowA)("Cross Hermit",0);
  local_c = FUN__text__0056ce80();
  uStack_10 = 0x429432;
  FUN__text__0056ce80();
  return;
}

