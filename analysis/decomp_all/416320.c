
void FUN__text__00416320(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1 != (int *)0x0) {
    (**(code **)(*param_1 + 8))(param_1);
    FUN__text__0056ce80();
  }
  local_8 = 0x416367;
  FUN__text__0056ce80();
  return;
}

