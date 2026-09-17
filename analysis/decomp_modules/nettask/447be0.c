
void __fastcall FUN__text__00447be0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 1;
  *(undefined4 *)(param_1 + 0x1bb4) = 0;
  local_8 = param_1;
  while (local_c != 0) {
    local_10 = *(int *)(local_8 + 0x1bb4);
    if (local_10 == 0) {
      FUN__text__004107b0();
      FUN__text__00410870(0x1e);
      *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
    }
    else if (local_10 == 1) {
      iVar1 = FUN__text__00410a60();
      if (iVar1 != 0) {
        *(int *)(local_8 + 0x1bb4) = *(int *)(local_8 + 0x1bb4) + 1;
      }
    }
    else if (local_10 == 2) {
      local_c = 0;
    }
    FUN__text__004481b0();
    FUN__text__00410b10(2);
    FUN__text__00422360(0);
  }
  FUN__text__004109e0(0);
  local_8 = 0x447cf3;
  FUN__text__0056ce80();
  return;
}

