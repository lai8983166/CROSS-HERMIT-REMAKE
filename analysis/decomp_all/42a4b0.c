
void FUN__text__0042a4b0(undefined4 param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 == 1) {
    (*API_USER32_DLL_SendMessageA)(param_1,0x466,1,param_4);
    FUN__text__0056ce80();
  }
  uStack_8 = 0x42a4fb;
  FUN__text__0056ce80();
  return;
}

