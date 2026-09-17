
void __thiscall FUN__text__00413e80(int param_1,int param_2)

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
  if (((*(int *)(param_1 + 0xb210) != 0) && (*(int *)(param_1 + 0xb250) != 0)) &&
     (*(int *)(param_1 + 0xb204) == param_2)) {
    local_8 = param_1;
    FUN__text__00413f00();
  }
  local_8 = 0x413efa;
  FUN__text__0056ce80();
  return;
}

