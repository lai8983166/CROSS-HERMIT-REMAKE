
void FUN__text__004297a0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [14];
  undefined4 uStack_c;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_SHLWAPI_DLL_PathAddBackslashA)(param_1);
  FUN__text__0056ce80();
  uStack_c = 0x4297db;
  FUN__text__0056ce80();
  return;
}

