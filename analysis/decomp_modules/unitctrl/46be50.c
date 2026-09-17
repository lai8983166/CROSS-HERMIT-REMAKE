
void __thiscall
FUN__text__0046be50(int param_1,int param_2,undefined4 param_3,undefined4 param_4,undefined4 param_5
                   )

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN__text__00465140(param_2 + 0x48,*(undefined4 *)(param_1 + 0x2a6e8),param_3,param_4,param_5,7);
  local_8 = 0x46bea4;
  FUN__text__0056ce80();
  return;
}

