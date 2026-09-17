
void __fastcall FUN__text__0044ffa0(int param_1)

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
  *(undefined4 *)(param_1 + 0x1108) = 0;
  local_8 = param_1;
  if (*(int *)(param_1 + 0x8e4) != 0) {
    local_c = *(undefined4 *)(param_1 + 0x8e4);
    FUN__text__00428ad0(local_c);
    *(undefined4 *)(local_8 + 0x8e4) = 0;
  }
  FUN__text__00428c00();
  local_8 = 0x450018;
  FUN__text__0056ce80();
  return;
}

