
void FUN__text__00480740(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(char *)(*(int *)(param_1 + 600) + 0x97) != '\0') &&
     (local_10 = FUN__text__00480640(param_1), local_10 != 0)) {
    local_c = FUN__text__00480540(param_1);
  }
  local_8 = 0x4807d7;
  FUN__text__0056ce80();
  return;
}

