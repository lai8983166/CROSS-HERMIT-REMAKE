
void FUN__text__0042a240(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        ,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [11];
  undefined4 uStack_18;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_GDI32_DLL_MoveToEx)(param_1,param_2,param_3,0);
  iVar1 = FUN__text__0056ce80();
  if (iVar1 != 0) {
    (*API_GDI32_DLL_LineTo)(param_1,param_4,param_5);
    FUN__text__0056ce80();
  }
  uStack_18 = 0x42a2a1;
  FUN__text__0056ce80();
  return;
}

