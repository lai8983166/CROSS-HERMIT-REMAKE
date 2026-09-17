
void __fastcall FUN__text__00444820(int param_1)

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
  local_8 = param_1;
  _memset((void *)(param_1 + 0x1bb0),0,0x10);
  while (local_c != 0) {
    local_10 = *(int *)(local_8 + 0x1bb0);
    if (local_10 == 0) {
      FUN__text__004107b0();
      FUN__text__00410830(0x3c);
      *(int *)(local_8 + 0x1bb0) = *(int *)(local_8 + 0x1bb0) + 1;
    }
    else if (local_10 == 1) {
      iVar1 = FUN__text__00410a60();
      if (iVar1 != 0) {
        *(int *)(local_8 + 0x1bb0) = *(int *)(local_8 + 0x1bb0) + 1;
      }
    }
    else if (local_10 == 2) {
      *(undefined4 *)(local_8 + 0x1a50) = 5;
      local_c = 0;
    }
    FUN__text__0044ca80();
    FUN__text__0044c9a0(0);
    FUN__text__00410b10(2);
    FUN__text__00422360(0);
  }
  FUN__text__004109e0(0);
  local_8 = 0x444952;
  FUN__text__0056ce80();
  return;
}

