
void __fastcall FUN__text__00439c60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; local_8 = param_1, iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  while (*(int *)(local_8 + 0x48) != 0) {
    local_c = *(undefined4 *)(local_8 + 0x48);
    FUN__text__00427a80(local_c);
    FUN__text__00427cd0(local_c);
  }
  while (*(int *)(local_8 + 0x54) != 0) {
    local_c = *(undefined4 *)(local_8 + 0x54);
    FUN__text__00427a80(local_c);
    FUN__text__00427cd0(local_c);
  }
  local_8 = 0x439d04;
  FUN__text__0056ce80();
  return;
}

