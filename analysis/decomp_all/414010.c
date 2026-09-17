
void __fastcall FUN__text__00414010(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0xb210) != 0) {
    local_8 = param_1;
    (**(code **)(**(int **)(param_1 + 0xb210) + 0x1c))
              (*(undefined4 *)(param_1 + 0xb210),param_1 + 0xb314);
    local_c = FUN__text__0056ce80();
  }
  local_8 = 0x41408a;
  FUN__text__0056ce80();
  return;
}

