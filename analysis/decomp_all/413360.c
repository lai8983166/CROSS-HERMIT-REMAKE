
void FUN__text__00413360(void)

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
  FUN__text__00416140();
  if (*(int *)(local_8 + 0xb210) != 0) {
    (**(code **)(**(int **)(local_8 + 0xb210) + 8))(*(undefined4 *)(local_8 + 0xb210));
    local_c = FUN__text__0056ce80();
    *(undefined4 *)(local_8 + 0xb210) = 0;
  }
  if (*(int *)(local_8 + 0xb20c) != 0) {
    (**(code **)(**(int **)(local_8 + 0xb20c) + 8))(*(undefined4 *)(local_8 + 0xb20c));
    local_c = FUN__text__0056ce80();
    *(undefined4 *)(local_8 + 0xb20c) = 0;
  }
  if (*(int *)(local_8 + 0xb208) != 0) {
    (*API_GDI32_DLL_DeleteDC)(*(undefined4 *)(local_8 + 0xb208));
    FUN__text__0056ce80();
    *(undefined4 *)(local_8 + 0xb208) = 0;
  }
  local_8 = 0x413440;
  FUN__text__0056ce80();
  return;
}

