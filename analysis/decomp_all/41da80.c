
void FUN__text__0041da80(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__0041d790();
  if ((iVar1 != 0) && ((-0x2711 < param_1 || (0 < param_1)))) {
    *(int *)(local_8 + 0x250) = param_1;
    (**(code **)(**(int **)(local_8 + 0x10) + 0x1c))
              (*(undefined4 *)(local_8 + 0x10),*(undefined4 *)(local_8 + 0x250));
    local_c = FUN__text__0056ce80();
    if (local_c < 0) {
      FUN__text__0041d040(local_c);
    }
  }
  local_8 = 0x41db22;
  FUN__text__0056ce80();
  return;
}

