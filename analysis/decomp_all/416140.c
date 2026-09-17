
void __fastcall FUN__text__00416140(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN__text__00416320(*(undefined4 *)(param_1 + 0xb270));
  *(undefined4 *)(local_8 + 0xb270) = 0;
  if (*(int *)(local_8 + 0xb26c) != 0) {
    (*API_GDI32_DLL_DeleteObject)(*(undefined4 *)(local_8 + 0xb26c));
    FUN__text__0056ce80();
    *(undefined4 *)(local_8 + 0xb26c) = 0;
  }
  for (local_c = 0; local_c != 2; local_c = local_c + 1) {
    if (*(int *)(local_8 + 0x1090 + local_c * 4) != 0) {
      FUN__text__00401d30();
      FUN__text__00401e20();
      local_14 = *(int *)(local_8 + 0x1090 + local_c * 4);
      local_10 = local_14;
      if (local_14 == 0) {
        local_18 = 0;
      }
      else {
        local_18 = FUN__text__00416260(1);
      }
      *(undefined4 *)(local_8 + 0x1090 + local_c * 4) = 0;
    }
  }
  local_8 = 0x416251;
  FUN__text__0056ce80();
  return;
}

