
void __fastcall FUN__text__00473860(int param_1)

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
  DAT_007f450c = *(undefined2 *)(*(int *)(param_1 + 0x117c38) + 0x174);
  if (DAT_007f44ac == 0) {
    DAT_007f450e = 0;
  }
  else {
    local_c = *(int *)(param_1 + 0x2e6fc) - *(int *)(param_1 + 0x2e6f4);
    if (DAT_007f44ac < local_c) {
      if (DAT_007f44b0 < local_c) {
        DAT_007f450e = 3;
      }
      else {
        DAT_007f450e = 2;
      }
    }
    else {
      DAT_007f450e = 1;
    }
  }
  local_8 = param_1;
  iVar1 = FUN__text__004307b0();
  if (iVar1 == 0) {
    DAT_007f4510 = 1;
  }
  else {
    DAT_007f4510 = 2;
  }
  FUN__text__00473940();
  FUN__text__00473ab0();
  local_8 = 0x47392f;
  FUN__text__0056ce80();
  return;
}

