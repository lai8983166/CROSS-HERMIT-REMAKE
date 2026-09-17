
void __fastcall FUN__text__00413f00(int param_1)

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
  if ((*(int *)(param_1 + 0xb210) != 0) &&
     (local_8 = param_1, iVar1 = FUN__text__00416140(), iVar1 == 0)) {
    (**(code **)(**(int **)(local_8 + 0xb210) + 0x38))
              (*(undefined4 *)(local_8 + 0xb210),local_8 + 0xb234);
    local_c = FUN__text__0056ce80();
    FUN__text__00415f50();
  }
  local_8 = 0x413f93;
  FUN__text__0056ce80();
  return;
}

