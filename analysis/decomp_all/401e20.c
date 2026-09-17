
void __fastcall FUN__text__00401e20(int param_1)

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
  if (*(int *)(param_1 + 0x5c) != 0) {
    (**(code **)(**(int **)(param_1 + 0x5c) + 8))(*(undefined4 *)(param_1 + 0x5c));
    FUN__text__0056ce80();
    *(undefined4 *)(local_8 + 0x5c) = 0;
  }
  *(undefined4 *)(local_8 + 0x58) = 0;
  local_8 = 0x401e84;
  FUN__text__0056ce80();
  return;
}

