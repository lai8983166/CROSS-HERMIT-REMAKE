
void __thiscall FUN__text__00416cc0(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [13];
  undefined4 uStack_14;
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 0xb210) + 0x48))(*(undefined4 *)(param_1 + 0xb210),1,param_2);
  FUN__text__0056ce80();
  uStack_14 = 0x416d11;
  FUN__text__0056ce80();
  return;
}

