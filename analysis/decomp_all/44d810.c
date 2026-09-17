
void __fastcall FUN__text__0044d810(int param_1)

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
  local_c = *(undefined4 *)(param_1 + 0x30);
  local_8 = param_1;
  switch(local_c) {
  case 0:
    FUN__text__004107b0();
    FUN__text__00410830(0x1e);
    *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
    break;
  case 1:
    *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 1;
    break;
  case 2:
    iVar1 = FUN__text__00410a60();
    if (iVar1 != 0) {
      *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
    }
    break;
  case 3:
    iVar1 = FUN__text__0044dad0();
    if (iVar1 != 0) {
      *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
    }
    break;
  case 4:
    FUN__text__004107b0();
    FUN__text__00410870(0x1e);
    *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
    break;
  case 5:
    iVar1 = FUN__text__00410a60();
    if (iVar1 != 0) {
      *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
    }
    break;
  case 6:
  }
  local_8 = 0x44d94a;
  FUN__text__0056ce80();
  return;
}

