
void __thiscall FUN__text__00412a70(int param_1,int param_2)

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
  if (param_2 == 1) {
    if (*(int *)(param_1 + 4) != 0) {
      (**(code **)(**(int **)(param_1 + 4) + 0x1c))(*(undefined4 *)(param_1 + 4));
      FUN__text__0056ce80();
    }
    if (*(int *)(local_8 + 8) != 0) {
      (**(code **)(**(int **)(local_8 + 8) + 0x1c))(*(undefined4 *)(local_8 + 8));
      FUN__text__0056ce80();
    }
  }
  else {
    if (*(int *)(param_1 + 4) != 0) {
      (**(code **)(**(int **)(param_1 + 4) + 0x20))(*(undefined4 *)(param_1 + 4));
      FUN__text__0056ce80();
    }
    if (*(int *)(local_8 + 8) != 0) {
      (**(code **)(**(int **)(local_8 + 8) + 0x20))(*(undefined4 *)(local_8 + 8));
      FUN__text__0056ce80();
    }
  }
  local_8 = 0x412b34;
  FUN__text__0056ce80();
  return;
}

