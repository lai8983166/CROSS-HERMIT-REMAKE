
void FUN__text__0042c160(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [12];
  undefined4 uStack_14;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_WINMM_DLL_PlaySound)(0,0,0);
  FUN__text__0056ce80();
  uStack_14 = 0x42c19a;
  FUN__text__0056ce80();
  return;
}

