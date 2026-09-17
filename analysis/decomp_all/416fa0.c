
void FUN__text__00416fa0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [15];
  undefined4 uStack_c;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_KERNEL32_DLL_QueryPerformanceCounter)(param_1);
  FUN__text__0056ce80();
  uStack_c = 0x416fdd;
  FUN__text__0056ce80();
  return;
}

