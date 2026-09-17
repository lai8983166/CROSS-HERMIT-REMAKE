
void __fastcall FUN__text__004180b0(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*param_1 != 0) {
    FUN__text__00419240();
    FUN__text__00417cc0();
  }
  local_c = FUN__text__00417f60();
  local_8 = (int *)0x418100;
  FUN__text__0056ce80();
  return;
}

